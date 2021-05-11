import os
import sys

import networkx as nx
from github import Github, GithubException

import constants
import utils

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]

github = Github(ballerina_bot_token)

auto_bump = False
ballerina_version_regex = ""


def main():
    module_name_list = sort_module_name_list()
    print('Fetched module name list')
    module_details_json = initialize_module_details(module_name_list)
    print('Initialized module details')
    module_details_json = get_immediate_dependents(module_name_list, module_details_json)
    print('Fetched immediate dependents of each module')
    module_details_json = calculate_levels(module_name_list, module_details_json)
    print('Generated module dependency graph and updated module levels')
    module_details_json['modules'].sort(key=lambda s: s['level'])
    module_details_json = remove_modules_not_included_in_distribution(module_details_json)
    print('Removed central only modules and updated the list')

    try:
        utils.write_json_file(constants.EXTENSIONS_FILE, module_details_json)
    except Exception as e:
        print('Failed to write to extensions.json', e)
        sys.exit()

    print('Updated module details successfully')

    try:
        updated_file_content = open(constants.EXTENSIONS_FILE, 'r').read()
        update = utils.commit_file('ballerina-release',
                                   constants.EXTENSIONS_FILE, updated_file_content,
                                   constants.EXTENSIONS_UPDATE_BRANCH,
                                   '[Automated] Update Extensions Dependencies')
        if update:
            utils.open_pr_and_merge('ballerina-release',
                                    '[Automated] Update Extensions Dependencies',
                                    'Update dependencies in extensions.json',
                                    constants.EXTENSIONS_UPDATE_BRANCH)
        else:
            print('No changes to ' + constants.EXTENSIONS_FILE + ' file')
    except GithubException as e:
        print('Error occurred while committing extensions.json', e)
        sys.exit(1)
    print("Updated module details in 'ballerina-release' successfully")


# Sorts the ballerina extension module list in ascending order
def sort_module_name_list():
    global auto_bump
    global ballerina_version_regex

    try:
        name_list = utils.read_json_file(constants.MODULE_LIST_FILE)
    except Exception as e:
        print('Failed to read module_list.json', e)
        sys.exit()

    name_list['modules'].sort(key=lambda x: x['name'].split('-')[-1])

    try:
        utils.write_json_file(constants.MODULE_LIST_FILE, name_list)
    except Exception as e:
        print('Failed to write to file module_list.json', e)
        sys.exit()

    name_list['modules'].append({
        'name': 'ballerina-distribution'
    })
    auto_bump = name_list['auto_bump']
    ballerina_version_regex = name_list['lang_version_substring']

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
def remove_modules_in_intermediate_paths(g, source, destination, successors, module_details_json):
    longest_path = max(nx.all_simple_paths(g, source, destination), key=lambda x: len(x))

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
        g = nx.DiGraph()
    except Exception as e:
        print('Error generating graph', e)
        sys.exit()

    # Module names are used to create the nodes and the level attribute of the node is initialized to 0
    for module in module_name_list:
        g.add_node(module['name'], level=1)

    # Edges are created considering the dependents of each module
    for module in module_details_json['modules']:
        for dependent in module['dependents']:
            g.add_edge(module['name'], dependent)

    processing_list = []

    # Nodes with in degrees=0 and out degrees!=0 are marked as level 1 and the node is appended to the processing list
    for root in [node for node in g if g.in_degree(node) == 0 and g.out_degree(node) != 0]:
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
            for i in g.successors(node):
                successors.append(i)
            for successor in successors:
                remove_modules_in_intermediate_paths(g, node, successor, successors, module_details_json)
                g.nodes[successor]['level'] = level
                if successor not in temp:
                    temp.append(successor)
        processing_list = temp
        level = level + 1

    for module in module_details_json['modules']:
        module['level'] = g.nodes[module['name']]['level']

    return module_details_json


# Creates a JSON string to store module information
# returns: JSON with module details
def initialize_module_details(modules_list):
    global auto_bump
    global ballerina_version_regex

    module_details_json = {
        'auto_bump': auto_bump,
        'lang_version_substring': ballerina_version_regex,
        'modules': []
    }

    for module in modules_list:
        default_branch = get_default_branch(module['name'])

        artifact_name = module['name'].split('-')[-1]

        default_artifact_id = artifact_name + '-ballerina'
        default_version_key = 'stdlib' + artifact_name.capitalize() + 'Version'

        module_details_json['modules'].append({
            'name': module['name'],
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

    last_level = module_details_json['modules'][-1]['level']

    for module in module_details_json['modules']:
        if (module['name'] != 'ballerina-distribution' and not module['dependents'] and
                module['central_only_module']):
            removed_modules.append(module)

    for removed_module in removed_modules:
        module_details_json['modules'].remove(removed_module)
        removed_module['level'] = last_level + 1

    for module in module_details_json['modules']:
        module['central_only_module'] = False

    module_details_json['central_modules'] = removed_modules

    return module_details_json


main()
