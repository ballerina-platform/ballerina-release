import json
import os
import re
import sys
import time

import networkx as nx
from github import Github, InputGitAuthor, GithubException

import constants

EXTENSIONS_UPDATE_BRANCH = 'extensions_update'

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
ballerina_bot_email = os.environ[constants.ENV_BALLERINA_BOT_EMAIL]
ballerina_reviewer_bot_token = os.environ[constants.ENV_BALLERINA_REVIEWER_BOT_TOKEN]

github = Github(ballerina_bot_token)

auto_bump = False


def main():
    module_name_list = sort_module_name_list()
    print('Fetched module name list')
    module_details_json = initialize_module_details(module_name_list)
    print('Initialized module details and fetched latest module versions')
    module_details_json = get_immediate_dependents(module_name_list, module_details_json)
    print('Fetched immediate dependents of each module')
    module_details_json = calculate_levels(module_name_list, module_details_json)
    print('Generated module dependency graph and updated module levels')
    module_details_json['modules'].sort(key=lambda s: s['level'])
    module_details_json = remove_modules_not_included_in_distribution(module_details_json)
    print('Removed central only modules and updated the list')
    update_json_file(module_details_json)
    print('Updated module details successfully')
    commit_json_file()
    print("Updated module details in 'ballerina-release' successfully")


# Sorts the ballerina extension module list in ascending order
def sort_module_name_list():
    global auto_bump

    try:
        with open(constants.MODULE_LIST_FILE) as f:
            name_list = json.load(f)
    except Exception as e:
        print('Failed to read module_list.json', e)
        sys.exit()

    name_list['modules'].sort(key=lambda x: x['name'].split('-')[-1])

    try:
        with open(constants.MODULE_LIST_FILE, 'w') as json_file:
            json_file.seek(0)
            json.dump(name_list, json_file, indent=4)
            json_file.truncate()
    except Exception as e:
        print('Failed to write to file module_list.json', e)
        sys.exit()

    name_list['modules'].append({
        'name': 'ballerina-distribution'
    })
    auto_bump = name_list['auto_bump']

    return name_list['modules']


# Gets dependencies of ballerina extension module from build.gradle file in module repository
# returns: list of dependencies
def get_dependencies(module_name):
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module_name)
    gradle_file = repo.get_contents(constants.BUILD_GRADLE_FILE)
    data = gradle_file.decoded_content.decode(constants.ENCODING)

    dependencies = []

    for line in data.splitlines():
        if 'https://maven.pkg.github.com/ballerina-platform' in line:
            module = line.split('/')[-1][:-1]
            if module == module_name:
                continue
            dependencies.append(module)

    return dependencies


# Gets the version of the ballerina extension module from gradle.properties file in module repository
# returns: current version of the module
def get_version(module_name):
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module_name)
    properties_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE)
    data = properties_file.decoded_content.decode(constants.ENCODING)

    version = ''
    for line in data.splitlines():
        if re.match('version=', line):
            version = line.split('=')[-1]

    if version == '':
        print('Version not defined for ' + module_name)

    return version


# Gets the default branch of the extension repository
# returns: default branch name
def get_default_branch(module_name):
    try:
        repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module_name)
        return repo.default_branch
    except Exception as e:
        print('Failed to get repo details for ' + module_name, e)
        return ''


# Calculates the longest path between source and destination modules and replaces dependents that have intermediates
def remove_modules_in_intermediate_paths(G, source, destination, successors, module_details_json):
    longest_path = max(nx.all_simple_paths(G, source, destination), key=lambda x: len(x))

    for n in longest_path[1:-1]:
        if n in successors:
            for module in module_details_json['modules']:
                if module['name'] == source:
                    if destination in module['dependents']:
                        module['dependents'].remove(destination)
                    break


# Generates a directed graph using the dependencies of the modules
# Level of each module is calculated by traversing the graph 
# Returns a json string with updated level of each module
def calculate_levels(module_name_list, module_details_json):
    try:
        G = nx.DiGraph()
    except Exception as e:
        print('Error generating graph', e)
        sys.exit()

    # Module names are used to create the nodes and the level attribute of the node is initialized to 0
    for module in module_name_list:
        G.add_node(module['name'], level=1)

    # Edges are created considering the dependents of each module
    for module in module_details_json['modules']:
        for dependent in module['dependents']:
            G.add_edge(module['name'], dependent)

    processing_list = []

    # Nodes with in degrees=0 and out degrees!=0 are marked as level 1 and the node is appended to the processing list
    for root in [node for node in G if G.in_degree(node) == 0 and G.out_degree(node) != 0]:
        processing_list.append(root)

    # While the processing list is not empty, successors of each node in the current level are determined
    # For each successor of the node, 
    #    - Longest path from node to successor is considered and intermediate nodes are removed from dependent list
    #    - The level is updated and the successor is appended to a temporary array
    # After all nodes are processed in the current level the processing list is updated with the temporary array
    level = 2
    while len(processing_list) > 0:
        temp = []
        for node in processing_list:
            successors = []
            for i in G.successors(node):
                successors.append(i)
            for successor in successors:
                remove_modules_in_intermediate_paths(G, node, successor, successors, module_details_json)
                G.nodes[successor]['level'] = level
                if successor not in temp:
                    temp.append(successor)
        processing_list = temp
        level = level + 1

    for module in module_details_json['modules']:
        module['level'] = G.nodes[module['name']]['level']

    return module_details_json


# Updates the extensions.JSON file with dependents of each standard library module
def update_json_file(updated_json):
    try:
        with open(constants.EXTENSIONS_FILE, 'w') as json_file:
            json_file.seek(0)
            json.dump(updated_json, json_file, indent=4)
            json_file.truncate()
    except Exception as e:
        print('Failed to write to extensions.json', e)
        sys.exit()


# Creates a JSON string to store module information
# returns: JSON with module details
def initialize_module_details(modules_list):
    global auto_bump

    module_details_json = {
        'auto_bump': auto_bump,
        'modules': []
    }

    for module in modules_list:
        version = get_version(module['name'])
        default_branch = get_default_branch(module['name'])

        artifact_name = module['name'].split('-')[-1]

        default_artifact_id = artifact_name + '-ballerina'
        default_version_key = 'stdlib' + artifact_name.capitalize() + 'Version'

        module_details_json['modules'].append({
            'name': module['name'],
            'version': version,
            'level': 0,
            'group_id': module.get('group_id', 'org.ballerinalang'),
            'artifact_id': module.get('artifact_id', default_artifact_id),
            'version_key': module.get('version_key', default_version_key),
            'default_branch': default_branch,
            'auto_merge': module.get('auto_merge', True),
            'central_only_module': module.get('central_only_module', True),
            'dependents': []})
    # TODO: Add transitive dependencies
    return module_details_json


# Gets all the dependents of each module to generate the dependency graph
# returns: module details JSON with updated dependent details
def get_immediate_dependents(module_name_list, module_details_json):
    for module_name in module_name_list:
        dependencies = get_dependencies(module_name['name'])
        for module in module_details_json['modules']:
            if module['name'] in dependencies:
                module_details_json['modules'][module_details_json['modules'].index(module)]['dependents'].append(
                    module_name['name'])

    return module_details_json


def remove_modules_not_included_in_distribution(module_details_json):
    removed_modules = []

    for module in module_details_json['modules']:
        if (module['name'] != 'ballerina-distribution' and not module['dependents'] and
                module['central_only_module']):
            removed_modules.append(module)

    for removed_module in removed_modules:
        module_details_json['modules'].remove(removed_module)
        removed_module['level'] = 1

    for module in module_details_json['modules']:
        module['central_only_module'] = False

    module_details_json['central_modules'] = removed_modules

    return module_details_json


def commit_json_file():
    author = InputGitAuthor(ballerina_bot_username, ballerina_bot_email)

    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/ballerina-release')

    remote_file = ''
    try:
        contents = repo.get_contents('dependabot')
        while len(contents) > 0:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path == constants.EXTENSIONS_FILE:
                    remote_file = file_content
                    break
    except Exception as e:
        print('Error while accessing remote extensions.json', e)
        sys.exit(1)

    updated_file = open(constants.EXTENSIONS_FILE, 'r').read()
    remote_file_contents = remote_file.decoded_content.decode(constants.ENCODING)

    if updated_file == remote_file_contents:
        print('No changes to extensions.json file')
    else:
        try:
            base = repo.get_branch(repo.default_branch)
            branch = EXTENSIONS_UPDATE_BRANCH
            try:
                ref = f"refs/heads/" + branch
                repo.create_git_ref(ref=ref, sha=base.commit.sha)
            except:
                print("[Info] Unmerged update branch existed in 'ballerina-release'")
                branch = EXTENSIONS_UPDATE_BRANCH + '_tmp'
                ref = f"refs/heads/" + branch
                try:
                    repo.create_git_ref(ref=ref, sha=base.commit.sha)
                except GithubException as e:
                    print("[Info] deleting update tmp branch existed in 'ballerina-release'")
                    if e.status == 422:  # already exist
                        repo.get_git_ref("heads/" + branch).delete()
                        repo.create_git_ref(ref=ref, sha=base.commit.sha)
            repo.update_file(
                constants.EXTENSIONS_FILE,
                '[Automated] Update Extensions Dependencies',
                updated_file,
                remote_file.sha,
                branch=branch,
                author=author
            )
            if not branch == EXTENSIONS_UPDATE_BRANCH:
                update_branch = repo.get_git_ref("heads/" + EXTENSIONS_UPDATE_BRANCH)
                update_branch.edit(update["commit"].sha, force=True)
                repo.get_git_ref("heads/" + branch).delete()

        except Exception as e:
            print('Error while committing extensions.json', e)

        try:
            created_pr = repo.create_pull(
                title='Automated] Update Extensions Dependencies',
                body='Update dependencies in extensions.json',
                head=EXTENSIONS_UPDATE_BRANCH,
                base='master'
            )
        except Exception as e:
            print('Error occurred while creating pull request updating dependencies.', e)
            sys.exit(1)

        # To stop intermittent failures due to API sync
        time.sleep(5)

        r_github = Github(ballerina_reviewer_bot_token)
        repo = r_github.get_repo(constants.BALLERINA_ORG_NAME + '/ballerina-release')
        pr = repo.get_pull(created_pr.number)
        try:
            pr.create_review(event='APPROVE')
        except Exception as e:
            print('Error occurred while approving Update Extensions Dependencies PR', e)
            sys.exit(1)

        try:
            created_pr.merge()
        except Exception as e:
            print("Error occurred while merging dependency PR for module 'ballerina-release'", e)


main()
