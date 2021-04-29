import json
import os
import sys
import time
import urllib.request

from github import Github, InputGitAuthor, GithubException
from retry import retry

import constants

LANG_VERSION_KEY = 'ballerinaLangVersion'
LANG_VERSION_UPDATE_BRANCH = 'automated/dependency_version_update'

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
ballerina_bot_email = os.environ[constants.ENV_BALLERINA_BOT_EMAIL]
ballerina_reviewer_bot_token = os.environ[constants.ENV_BALLERINA_REVIEWER_BOT_TOKEN]

MODULE_CREATED_PR = 'created_pr'
MODULE_TIMESTAMPED_VERSION = 'timestamped_version'

MODULE_STATUS = 'status'
MODULE_STATUS_IN_PROGRESS = 'in_progress'
MODULE_STATUS_COMPLETED = 'completed'

MODULE_CONCLUSION = 'conclusion'
MODULE_CONCLUSION_TIMED_OUT = 'timed_out'
MODULE_CONCLUSION_PR_PENDING = 'pr_build_pending'
MODULE_CONCLUSION_PR_CHECK_FAILURE = 'pr_check_failure'
MODULE_CONCLUSION_PR_NOT_MERGED = 'pr_not_merged'
MODULE_CONCLUSION_PR_MERGE_FAILURE = 'merge_failure'
MODULE_CONCLUSION_BUILD_PENDING = 'build_pending'
MODULE_CONCLUSION_BUILD_SUCCESS = 'build_success'
MODULE_CONCLUSION_BUILD_FAILURE = 'build_failure'
MODULE_CONCLUSION_BUILD_RELEASED = 'build_released'
MODULE_CONCLUSION_VERSION_CANNOT_BE_IDENTIFIED = 'version_not_identified'

COMMIT_MESSAGE_PREFIX = '[Automated] Update dependencies'
PULL_REQUEST_BODY_PREFIX = 'Update ballerina lang version to `'
PULL_REQUEST_TITLE = '[Automated] Update Dependencies (Ballerina Lang : '
AUTO_MERGE_PULL_REQUEST_TITLE = '[AUTO MERGE] Update Dependencies (Ballerina Lang : '

SLEEP_INTERVAL = 30  # 30s
MAX_WAIT_CYCLES = 120

retrigger_dependency_bump = sys.argv[1]
override_ballerina_version = sys.argv[2]
auto_merge_pull_requests = sys.argv[3]

event_type = 'workflow_dispatch'
if len(sys.argv) > 4:
    event_type = sys.argv[4]

github = Github(ballerina_bot_token)

extensions_file = {}
all_modules = []
current_level_modules = []
lang_version = ''
status_completed_modules = 0


def main():
    global lang_version
    global extensions_file
    global all_modules

    lang_version = get_lang_version()
    update_workflow_lang_version()
    commit_json_file()

    print('Workflow started with Ballerina Lang version : ' + lang_version)
    extensions_file = get_extensions_file()

    print("Workflow invoked of type '" + event_type + "'")
    if event_type == 'schedule' and not extensions_file['auto_bump']:
        print("Schedule workflow invoked, exiting script as 'auto_bump' flag in modules_list.json is false.")
        return

    print('Start dependency bump to extensions packed in ballerina-distribution')
    all_modules = extensions_file['modules']
    check_and_update_lang_version()
    print('Successfully bumped dependencies in extensions packed in ballerina-distribution')

    print('Start dependency bump to extensions available only in central')
    all_modules = extensions_file['central_modules']
    check_and_update_lang_version()
    print('Successfully bumped dependencies in extensions available in central')


def get_lang_version():
    if override_ballerina_version != '':
        return override_ballerina_version
    else:
        try:
            version_string = open_url(
                'https://api.github.com/orgs/ballerina-platform/packages/maven/org.ballerinalang.jballerina-tools/versions').read()
        except Exception as e:
            print('[Error] Failed to get ballerina packages version', e)
            sys.exit(1)
        latest_version = json.loads(version_string)[0]
        return latest_version['name']


@retry(
    urllib.error.URLError,
    tries=constants.HTTP_REQUEST_RETRIES,
    delay=constants.HTTP_REQUEST_DELAY_IN_SECONDS,
    backoff=constants.HTTP_REQUEST_DELAY_MULTIPLIER
)
def open_url(url):
    request = urllib.request.Request(url)
    request.add_header('Accept', 'application/vnd.github.v3+json')
    request.add_header('Authorization', 'Bearer ' + ballerina_bot_token)

    return urllib.request.urlopen(request)


def get_extensions_file():
    try:
        with open(constants.EXTENSIONS_FILE) as f:
            module_list = json.load(f)

    except Exception as e:
        print('[Error] Error while loading modules list ', e)
        sys.exit(1)

    return module_list


def check_and_update_lang_version():
    global all_modules

    module_details_list = all_modules
    module_details_list.sort(reverse=True, key=lambda s: s['level'])
    last_level = module_details_list[0]['level']

    for i in range(last_level):
        current_level = i + 1
        global current_level_modules
        current_level_modules = list(filter(lambda s: s['level'] == current_level, all_modules))

        for idx, module in enumerate(current_level_modules):
            print("[Info] Check lang dependency in module '" + module['name'] + "'")
            update_module(idx, current_level)

        if auto_merge_pull_requests.lower() == 'true':
            wait_for_current_level_build(current_level)


def wait_for_current_level_build(level):
    global MAX_WAIT_CYCLES

    print("[Info] Waiting for level '" + str(level) + "' module build.")
    total_modules = len(current_level_modules)

    if level == 6:
        # Level 6 & Level 7 modules take about 40 minutes each for PR build and build
        MAX_WAIT_CYCLES = 2 * MAX_WAIT_CYCLES

    wait_cycles = 0
    global status_completed_modules
    status_completed_modules = 0

    while status_completed_modules != total_modules:
        for idx, module in enumerate(current_level_modules):
            if module[MODULE_STATUS] == MODULE_STATUS_IN_PROGRESS:
                if module[MODULE_CONCLUSION] == MODULE_CONCLUSION_PR_PENDING:
                    check_pending_pr_checks(idx)
                else:
                    # Build checks test
                    check_pending_build_checks(idx)

        if wait_cycles < MAX_WAIT_CYCLES:
            time.sleep(SLEEP_INTERVAL)
            wait_cycles = wait_cycles + 1
        else:
            # Force stop script with all in progress modules printed
            print('Dependency bump script timed out. Following modules are in pending state')
            for module in current_level_modules:
                if module[MODULE_STATUS] == MODULE_STATUS_IN_PROGRESS:
                    print(module['name'])
            sys.exit(1)

    module_release_failure = False
    pr_checks_failed_modules = list(
        filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_PR_CHECK_FAILURE, current_level_modules))
    if len(pr_checks_failed_modules) != 0:
        module_release_failure = True
        print('Following modules dependency PRs have failed checks...')
        for module in pr_checks_failed_modules:
            print(module['name'])

    pr_merged_failed_modules = list(
        filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_PR_MERGE_FAILURE, current_level_modules))
    if len(pr_merged_failed_modules) != 0:
        module_release_failure = True
        print('Following modules dependency PRs could not be merged...')
        for module in pr_merged_failed_modules:
            print(module['name'])

    build_checks_failed_modules = list(
        filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_BUILD_FAILURE, current_level_modules))
    if len(build_checks_failed_modules) != 0:
        module_release_failure = True
        print('Following modules timestamped build checks failed...')
        for module in build_checks_failed_modules:
            print(module['name'])

    build_version_failed_modules = list(
        filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_VERSION_CANNOT_BE_IDENTIFIED, current_level_modules))
    if len(build_version_failed_modules) != 0:
        module_release_failure = True
        print('Following modules timestamped build version cannot be identified...')
        for module in build_version_failed_modules:
            print(module['name'])

    if module_release_failure:
        sys.exit(1)


def check_pending_pr_checks(index: int):
    module = current_level_modules[index]
    global status_completed_modules
    print("[Info] Checking the status of the dependency bump PR in module '" + module['name'] + "'")
    passing = True
    pending = False
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module['name'])

    failed_pr_checks = []
    pull_request = repo.get_pull(module[MODULE_CREATED_PR].number)
    sha = pull_request.head.sha
    for pr_check in repo.get_commit(sha=sha).get_check_runs():
        # Ignore codecov checks temporarily due to bug
        if not pr_check.name.startswith('codecov'):
            if pr_check.status != 'completed':
                pending = True
                break
            elif pr_check.conclusion == 'success':
                continue
            elif (module['name'] == 'module-ballerinax-jaeger' and
                  pr_check.conclusion == 'skipped'):
                continue
            else:
                failed_pr_check = {
                    'name': pr_check.name,
                    'html_url': pr_check.html_url
                }
                failed_pr_checks.append(failed_pr_check)
                passing = False
    if not pending:
        if passing:
            if module['auto_merge'] & ('AUTO MERGE' in pull_request.title):
                try:
                    pull_request.merge()
                    print("[Info] Automated version bump PR merged for module '" + module[
                        'name'] + "'. PR: " + pull_request.html_url)
                    current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_PENDING
                except Exception as e:
                    print("[Error] Error occurred while merging dependency PR for module '" +
                          current_level_modules[index]['name'] + "'", e)
                    current_level_modules[index][MODULE_STATUS] = MODULE_STATUS_COMPLETED
                    current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_PR_MERGE_FAILURE
                    status_completed_modules += 1
            else:
                current_level_modules[index][MODULE_STATUS] = MODULE_STATUS_COMPLETED
                current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_PR_NOT_MERGED
                status_completed_modules += 1

        else:
            current_level_modules[index][MODULE_STATUS] = MODULE_STATUS_COMPLETED
            current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_PR_CHECK_FAILURE
            module_name = module['name']
            print("[Error] Dependency bump PR checks have failed for '" + module_name + "'")
            for check in failed_pr_checks:
                print("[" + module_name + "] PR check '" + check["name"] + "' failed for " + check["html_url"])
            status_completed_modules += 1


def check_pending_build_checks(index: int):
    module = current_level_modules[index]
    global status_completed_modules
    print("[Info] Checking the status of the timestamped build in module '" + module['name'] + "'")
    passing = True
    pending = False
    build_check_found = False  # This is to stop intermittent failures
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module['name'])
    pull_request = repo.get_pull(module[MODULE_CREATED_PR].number)
    sha = pull_request.merge_commit_sha

    failed_build_name, failed_build_html = [], []
    if module[MODULE_CONCLUSION] == MODULE_CONCLUSION_BUILD_PENDING:
        for build_check in repo.get_commit(sha=sha).get_check_runs():
            build_check_found = True
            # Ignore codecov checks temporarily due to bug
            if not build_check.name.startswith('codecov'):
                if build_check.status != 'completed':
                    pending = True
                    break
                elif build_check.conclusion == 'success':
                    continue
                else:
                    failed_build_name.append(build_check.name)
                    failed_build_html.append(build_check.html_url)
                    passing = False
        if build_check_found and not pending:
            if passing:
                current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_SUCCESS
            else:
                current_level_modules[index][MODULE_STATUS] = MODULE_STATUS_COMPLETED
                current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_FAILURE
                module_name = module['name']
                print("[Error] Dependency bump PR merge build checks have failed for '" + module_name + "'")
                for name, html_url in zip(failed_build_name, failed_build_html):
                    print("[" + module_name + "] Build check '" + name + "' failed for " + html_url)
                status_completed_modules += 1
    else:
        # Already successful and merged
        current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_SUCCESS

    if current_level_modules[index][MODULE_CONCLUSION] == MODULE_CONCLUSION_BUILD_SUCCESS:
        if current_level_modules[index]['name'] == 'ballerina-distribution':
            current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_RELEASED
        else:
            try:
                packages_list_string = open_url(
                    'https://api.github.com/orgs/' + constants.BALLERINA_ORG_NAME + '/packages/maven/' + module[
                        'group_id'] + '.' + module['artifact_id'] + '/versions').read()
                packages_list = json.loads(packages_list_string)
                latest_package = packages_list[0]['name']

                if retrigger_dependency_bump.lower() == 'true':
                    for package in packages_list:
                        sha_of_released_package = package['name'].split('-')[-1]
                        if sha_of_released_package in sha:
                            latest_package = package['name']
                            break

                current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_RELEASED
                current_level_modules[index][MODULE_TIMESTAMPED_VERSION] = latest_package
            except Exception as e:
                print("[Error] Failed to get latest timestamped version for module '" + module['name'] + "'", e)
                current_level_modules[index][MODULE_STATUS] = MODULE_CONCLUSION_VERSION_CANNOT_BE_IDENTIFIED
        current_level_modules[index][MODULE_STATUS] = MODULE_STATUS_COMPLETED
        status_completed_modules += 1


def update_module(idx: int, current_level):
    module = current_level_modules[idx]
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module['name'])
    properties_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE)

    properties_file = properties_file.decoded_content.decode(constants.ENCODING)
    update, updated_properties_file = get_updated_properties_file(module['name'], current_level, properties_file)
    if update:
        commit_changes(repo, updated_properties_file, module['name'])
        create_pull_request(idx, repo)
    else:
        current_level_modules[idx][MODULE_STATUS] = MODULE_STATUS_IN_PROGRESS
        current_level_modules[idx][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_PENDING
        current_level_modules[idx][MODULE_CREATED_PR] = None

        pulls = repo.get_pulls(state='closed')
        sha_of_lang = lang_version.split('-')[-1]

        for pull in pulls:
            if sha_of_lang in pull.title:
                current_level_modules[idx][MODULE_CREATED_PR] = pull
                break


def get_updated_properties_file(module_name, current_level, properties_file):
    updated_properties_file = ''
    update = False

    split_lang_version = lang_version.split('-')
    processed_lang_version = split_lang_version[2] + split_lang_version[3]

    for line in properties_file.splitlines():
        if line.startswith(LANG_VERSION_KEY):
            current_version = line.split('=')[-1]

            split_current_version = current_version.split('-')

            if len(split_current_version) > 3:
                processed_current_version = split_current_version[2] + split_current_version[3]

                if processed_current_version < processed_lang_version:
                    print("[Info] Updating the lang version in module: '" + module_name + "'")
                    updated_properties_file += LANG_VERSION_KEY + '=' + lang_version + '\n'
                    update = True
                else:
                    updated_properties_file += line + '\n'
            else:
                # Stable dependency & SNAPSHOT
                print("[Info] Updating the lang version in module: '" + module_name + "'")
                updated_properties_file += LANG_VERSION_KEY + '=' + lang_version + '\n'
                update = True
        else:
            key_found = False
            possible_dependency_modules = list(filter(lambda s: s['level'] < current_level, all_modules))

            for possible_dependency in possible_dependency_modules:
                if line.startswith(possible_dependency['version_key']):
                    updated_line = possible_dependency['version_key'] + '=' + possible_dependency[
                        MODULE_TIMESTAMPED_VERSION]
                    updated_properties_file += updated_line + '\n'
                    key_found = True
                    if line != updated_line:
                        update = True
                    break
            if not key_found:
                updated_properties_file += line + '\n'

    if update:
        print("[Info] Update lang dependency in module '" + module_name + "'")
    return update, updated_properties_file


def commit_changes(repo, updated_file, module_name):
    author = InputGitAuthor(ballerina_bot_username, ballerina_bot_email)
    base = repo.get_branch(repo.default_branch)
    branch = LANG_VERSION_UPDATE_BRANCH

    try:
        ref = f"refs/heads/" + branch
        repo.create_git_ref(ref=ref, sha=base.commit.sha)
    except:
        print("[Info] Unmerged update branch existed in module: '" + module_name + "'")
        branch = LANG_VERSION_UPDATE_BRANCH + '_tmp'
        ref = f"refs/heads/" + branch
        try:
            repo.create_git_ref(ref=ref, sha=base.commit.sha)
        except GithubException as e:
            print("[Info] deleting update tmp branch existed in module: '" + module_name + "'")
            if e.status == 422:  # already exist
                repo.get_git_ref("heads/" + branch).delete()
                repo.create_git_ref(ref=ref, sha=base.commit.sha)

    remote_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE, ref=LANG_VERSION_UPDATE_BRANCH)
    remote_file_contents = remote_file.decoded_content.decode(constants.ENCODING)

    if remote_file_contents == updated_file:
        print('[Info] Branch with the lang version is already present.')
    else:
        current_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE, ref=branch)
        update = repo.update_file(
            current_file.path,
            COMMIT_MESSAGE_PREFIX,
            updated_file,
            current_file.sha,
            branch=branch,
            author=author
        )
        if not branch == LANG_VERSION_UPDATE_BRANCH:
            update_branch = repo.get_git_ref("heads/" + LANG_VERSION_UPDATE_BRANCH)
            update_branch.edit(update["commit"].sha, force=True)
            repo.get_git_ref("heads/" + branch).delete()


def create_pull_request(idx: int, repo):
    module = current_level_modules[idx]
    pulls = repo.get_pulls(state='open')
    pr_exists = False
    created_pr = ''

    sha_of_lang = lang_version.split('-')[-1]

    for pull in pulls:
        if pull.head.ref == LANG_VERSION_UPDATE_BRANCH:
            pr_exists = True
            created_pr = pull
            pull.edit(
                title=pull.title.rsplit('-', 1)[0] + '-' + sha_of_lang + ')',
                body=pull.body.rsplit('-', 1)[0] + '-' + sha_of_lang + '` and relevant extensions.'
            )
            print("[Info] Automated version bump PR found for module '" + module['name'] + "'. PR: " + pull.html_url)
            break

    if not pr_exists:
        try:
            pull_request_title = PULL_REQUEST_TITLE
            if (auto_merge_pull_requests.lower() == 'true') & module['auto_merge']:
                pull_request_title = AUTO_MERGE_PULL_REQUEST_TITLE
            pull_request_title = pull_request_title + lang_version + ')'

            created_pr = repo.create_pull(
                title=pull_request_title,
                body=PULL_REQUEST_BODY_PREFIX + lang_version + '` and relevant extensions.',
                head=LANG_VERSION_UPDATE_BRANCH,
                base=repo.default_branch
            )
            print("[Info] Automated version bump PR created for module '" + module[
                'name'] + "'. PR: " + created_pr.html_url)
        except Exception as e:
            print("[Error] Error occurred while creating pull request for module '" + module['name'] + "'.", e)
            sys.exit(1)

        if (auto_merge_pull_requests.lower() == 'true') & module['auto_merge']:

            # To stop intermittent failures due to API sync
            time.sleep(5)

            r_github = Github(ballerina_reviewer_bot_token)
            repo = r_github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module['name'])
            pr = repo.get_pull(created_pr.number)
            try:
                pr.create_review(event='APPROVE')
                print(
                    "[Info] Automated version bump PR approved for module '" + module['name'] + "'. PR: " + pr.html_url)
            except Exception as e:
                print("[Error] Error occurred while approving dependency PR for module '" + module['name'] + "'",
                      e)

    current_level_modules[idx][MODULE_CREATED_PR] = created_pr
    current_level_modules[idx][MODULE_STATUS] = MODULE_STATUS_IN_PROGRESS
    current_level_modules[idx][MODULE_CONCLUSION] = MODULE_CONCLUSION_PR_PENDING


def update_workflow_lang_version():
    bal_version = {
        'version': lang_version
    }
    try:
        with open(constants.LANG_VERSION_FILE, 'w') as json_file:
            json_file.seek(0)
            json.dump(bal_version, json_file, indent=4)
            json_file.truncate()
    except Exception as e:
        print('Failed to write to file latest_ballerina_lang_version.json', e)
        sys.exit()


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
                if file_content.path == constants.LANG_VERSION_FILE:
                    remote_file = file_content
                    break
    except Exception as e:
        print('Error while accessing remote lang-version.json', e)
        sys.exit(1)

    updated_file = open(constants.LANG_VERSION_FILE, 'r').read()
    remote_file_contents = remote_file.decoded_content.decode(constants.ENCODING)

    if updated_file == remote_file_contents:
        print('No changes to latest-ballerina-lang-version.json file')
    else:
        try:
            base = repo.get_branch(repo.default_branch)
            branch = constants.EXTENSIONS_UPDATE_BRANCH
            try:
                ref = f"refs/heads/" + branch
                repo.create_git_ref(ref=ref, sha=base.commit.sha)
            except:
                print("[Info] Unmerged update branch existed in 'ballerina-release'")
                branch = constants.EXTENSIONS_UPDATE_BRANCH + '_tmp'
                ref = f"refs/heads/" + branch
                try:
                    repo.create_git_ref(ref=ref, sha=base.commit.sha)
                except GithubException as e:
                    print("[Info] deleting update tmp branch existed in 'ballerina-release'")
                    if e.status == 422:  # already exist
                        repo.get_git_ref("heads/" + branch).delete()
                        repo.create_git_ref(ref=ref, sha=base.commit.sha)
            update = repo.update_file(
                constants.LANG_VERSION_FILE,
                '[Automated] Update Workflow Lang Version',
                updated_file,
                remote_file.sha,
                branch=branch,
                author=author
            )
            if not branch == constants.EXTENSIONS_UPDATE_BRANCH:
                update_branch = repo.get_git_ref("heads/" + constants.EXTENSIONS_UPDATE_BRANCH)
                update_branch.edit(update["commit"].sha, force=True)
                repo.get_git_ref("heads/" + branch).delete()

        except Exception as e:
            print('Error while committing workflow lang version', e)

        try:
            created_pr = repo.create_pull(
                title='[Automated] Update Dependency Bump Workflow Triggered Version',
                body='Update bumped ballerina lang version',
                head=constants.EXTENSIONS_UPDATE_BRANCH,
                base='master'
            )
        except Exception as e:
            print('Error occurred while creating pull request updating workflow lang version.', e)
            sys.exit(1)

        # To stop intermittent failures due to API sync
        time.sleep(5)

        r_github = Github(ballerina_reviewer_bot_token)
        repo = r_github.get_repo(constants.BALLERINA_ORG_NAME + '/ballerina-release')
        pr = repo.get_pull(created_pr.number)
        try:
            pr.create_review(event='APPROVE')
        except Exception as e:
            print('Error occurred while approving Update Dependency Bump Workflow Triggered Version PR', e)
            sys.exit(1)

        try:
            created_pr.merge()
        except Exception as e:
            print("Error occurred while merging Update Dependency Bump Workflow Triggered Version", e)
            sys.exit(1)


main()
