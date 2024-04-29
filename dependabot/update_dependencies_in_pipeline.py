import json
import os
import sys
import time

from github import Github, GithubException

import constants
import notify_chat
import utils

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]

MODULE_BUILD_ACTION_FILE = "build_action_file"

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

COMMIT_MESSAGE = '[Automated] Update dependencies'
PULL_REQUEST_BODY_PREFIX = 'Update ballerina lang version to `'
PULL_REQUEST_TITLE = '[Automated] Update Dependencies (Ballerina Lang : '
AUTO_MERGE_PULL_REQUEST_TITLE = '[AUTO MERGE] Update Dependencies (Ballerina Lang : '

SLEEP_INTERVAL = 30  # 30s
MAX_WAIT_CYCLES = 120  # Initial timeout is 1h, changed to 80 & 140 m in level 5 & 6 respectively

retrigger_dependency_bump = sys.argv[1]
skip_lang_update = sys.argv[2]
override_ballerina_version = sys.argv[3]
auto_merge_pull_requests = sys.argv[4]
send_notification = sys.argv[5]

event_type = 'workflow_dispatch'
if len(sys.argv) > 6:
    event_type = sys.argv[6]

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
    global current_level_modules

    try:
        extensions_file = utils.read_json_file(constants.EXTENSIONS_FILE)
    except Exception as e:
        print('[Error] Error while loading modules list ', e)
        sys.exit(1)

    print("Workflow invoked of type '" + event_type + "'")
    if event_type == 'schedule' and not extensions_file['auto_bump']:
        print("Schedule workflow invoked, exiting script as 'auto_bump' flag in modules_list.json is false.")
        return

    if override_ballerina_version != '':
        lang_version = override_ballerina_version
    else:
        lang_version = utils.get_latest_lang_version()

    bal_version = {
        'version': lang_version
    }

    if not skip_lang_update:
        try:
            utils.write_json_file(constants.LANG_VERSION_FILE, bal_version)
        except Exception as e:
            print('Failed to write to file latest_ballerina_lang_version.json', e)
            sys.exit()

        try:
            updated_file_content = open(constants.LANG_VERSION_FILE, 'r').read()
            update = utils.commit_file('ballerina-release',
                                       constants.LANG_VERSION_FILE, updated_file_content,
                                       constants.EXTENSIONS_UPDATE_BRANCH,
                                       '[Automated] Update Workflow Lang Version')[0]
            if update:
                utils.open_pr_and_merge('ballerina-release',
                                        '[Automated] Update Workflow Triggered Ballerina Version',
                                        'Update workflow triggered ballerina lang version',
                                        constants.EXTENSIONS_UPDATE_BRANCH)
            else:
                print('No changes to ' + constants.LANG_VERSION_FILE + ' file')
        except GithubException as e:
            print('Error occurred while committing latest_ballerinalang_version.md', e)
            sys.exit(1)

    print('Workflow started with Ballerina Lang version : ' + lang_version)

    all_modules = extensions_file['standard_library']

    last_level = all_modules[-1]['level']

    print('Start dependency update for Ballerina Standard Library')
    for i in range(last_level):
        current_level = i + 1
        current_level_modules = list(filter(lambda s: s['level'] == current_level, all_modules))

        for idx, module in enumerate(current_level_modules):
            print("[Info] Check lang dependency in module '" + module['name'] + "'")
            update_module(idx, current_level)

        if auto_merge_pull_requests.lower() == 'true':
            wait_for_current_level_build(current_level, True)
    print('Successfully updated dependencies in Ballerina Standard Library')

    extended_library_level = extensions_file['extended_library'][-1]['level']

    print('Start dependency update for Ballerina library')
    for j in range(last_level, extended_library_level):
        current_level = j + 1
        current_level_modules = list(filter(lambda s: s['level'] == current_level, extensions_file['extended_library']))

        for idx, module in enumerate(current_level_modules):
            print("[Info] Check lang dependency in module '" + module['name'] + "'")
            update_module(idx, current_level)

        if auto_merge_pull_requests.lower() == 'true':
            wait_for_current_level_build(current_level, False)
    print('Successfully updated dependencies in Ballerina Extended Library')


def wait_for_current_level_build(level, is_stdlib_module):
    global MAX_WAIT_CYCLES
    global send_notification
    global status_completed_modules

    print("[Info] Waiting for level '" + str(level) + "' module build.")
    total_modules = len(current_level_modules)

    if level == 5:
        # In level 5 http takes around 30 min for PR build and build each
        # Changes timeout to 80 minutes
        MAX_WAIT_CYCLES = 140

    if level == 6:
        # In level 6 c2c takes around 52 min for PR build and build each
        # Changes timeout to 140 minutes
        MAX_WAIT_CYCLES = 280

    wait_cycles = 0
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
            print('Dependency update script timed out. Following modules are in pending state')
            for module in current_level_modules:
                if module[MODULE_STATUS] == MODULE_STATUS_IN_PROGRESS:
                    print(module['name'])
            sys.exit(1)

    module_release_failure = False
    chat_message_send = False
    chat_message = "Dependency update to lang version *" + lang_version + "*\n\n"
    print()
    pr_checks_failed_modules = list(filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_PR_CHECK_FAILURE, current_level_modules))
    if len(pr_checks_failed_modules) != 0:
        module_release_failure = True
        pr_failed_message = 'Following modules\' Automated Dependency Update PRs have failed checks...'
        send_chat, partial_chat_message = get_chat_message(pr_checks_failed_modules, pr_failed_message, True)
        chat_message_send = chat_message_send or send_chat
        chat_message += partial_chat_message

    pr_merged_failed_modules = list(filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_PR_MERGE_FAILURE, current_level_modules))
    if len(pr_merged_failed_modules) != 0:
        module_release_failure = True
        pr_merged_failed_message = 'Following modules\' Automated Dependency Update PRs could not be merged...'
        send_chat, partial_chat_message = get_chat_message(pr_merged_failed_modules, pr_merged_failed_message, True)
        chat_message_send = chat_message_send or send_chat
        chat_message += partial_chat_message

    build_checks_failed_modules = list(filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_BUILD_FAILURE, current_level_modules))
    if len(build_checks_failed_modules) != 0:
        module_release_failure = True
        build_checks_failed_message = 'Following modules\' Timestamped Build checks have failed...'
        send_chat, partial_chat_message = get_chat_message(build_checks_failed_modules, build_checks_failed_message, False)
        chat_message_send = chat_message_send or send_chat
        chat_message += partial_chat_message

    build_version_failed_modules = list(filter(lambda s: s[MODULE_CONCLUSION] == MODULE_CONCLUSION_VERSION_CANNOT_BE_IDENTIFIED, current_level_modules))
    if len(build_version_failed_modules) != 0:
        module_release_failure = True
        build_version_failed_message = 'Following modules\' latest Timestamped Build Version cannot be identified...'
        send_chat, partial_chat_message = get_chat_message(build_version_failed_modules, build_version_failed_message, False)
        chat_message_send = chat_message_send or send_chat
        chat_message += partial_chat_message

    if is_stdlib_module:
        chat_message += "After following up on the above, trigger the <" + \
                        "https://github.com/ballerina-platform/ballerina-release/actions/workflows/update_dependency_version.yml" + \
                        "|Dependency Update Workflow>"

    if send_notification == 'true' and chat_message_send:
        print('Failing modules that is being notified:')
        print(utils.get_sanitised_chat_message(chat_message))
        notify_chat.send_message(chat_message)
    elif chat_message_send:
        print('Failing modules that is NOT being notified:')
        print(utils.get_sanitised_chat_message(chat_message))

    if module_release_failure:
        sys.exit(1)


def get_chat_message(modules, log_start, pr_link):
    print_log_modules = list(filter(lambda s: s['send_notification'] is False, modules))
    if len(print_log_modules) > 0:
        print(log_start + '\n')
        for failed_module in print_log_modules:
            if pr_link:
                link = failed_module[MODULE_CREATED_PR].html_url
            else:
                link = constants.BALLERINA_ORG_URL + failed_module['name'] + "/actions/workflows/" + \
                       failed_module[MODULE_BUILD_ACTION_FILE] + ".yml"
            print(failed_module['name'] + ' (' + link + ')')
        print()

    send_chat = False
    chat_message = ''
    notification_modules = list(filter(lambda s: s['send_notification'] is True, modules))
    if len(notification_modules) > 0:
        send_chat = True
        chat_message = log_start + '\n'
        for notification_module in notification_modules:
            if pr_link:
                link = notification_module[MODULE_CREATED_PR].html_url
            else:
                link = constants.BALLERINA_ORG_URL + notification_module['name'] + "/actions/workflows/" + \
                       notification_module[MODULE_BUILD_ACTION_FILE] + ".yml"
            chat_message += utils.get_module_message(notification_module, link)
        chat_message += '\n'

    return send_chat, chat_message


def check_pending_pr_checks(index: int):
    module = current_level_modules[index]
    global status_completed_modules
    print("[Info] Checking the status of the dependency update PR in module '" + module['name'] + "'")
    passing = True
    pending = False
    codecov_complete = False
    count = 0
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module['name'])

    failed_pr_checks = []
    pull_request = repo.get_pull(module[MODULE_CREATED_PR].number)

    # Check if the PR is merged
    if pull_request.merged:
        log_message = "[Info] Automated version update PR merged for module '" + module['name'] \
                                  + "'. PR: " + pull_request.html_url
        print(log_message)
        current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_PENDING
        return

    sha = pull_request.head.sha
    for pr_check in repo.get_commit(sha=sha).get_check_runs():
        count += 1
        # Ignore codecov checks temporarily due to bug
        if not pr_check.name.startswith('codecov') and not pr_check.name.startswith('SonarCloud') and 'graalvm' not in pr_check.name:
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
        else:
            if pr_check.status == 'completed':
                codecov_complete = True
    if count < 1:
        # Here the checks have not been triggered yet.
        return
    if not pending:
        if passing:
            if module['auto_merge'] & ('AUTO MERGE' in pull_request.title):
                # Distribution does not have codecov checks, nether does ballerinai/observe
                if not (module['name'] == 'ballerina-distribution' or module['name'] == 'module-ballerinai-observe'
                    or module['name'] == 'module-ballerina-observe' or codecov_complete):
                    # Wait till the codecov checks pass before merge
                    return
                try:
                    pull_request.merge()
                    log_message = "[Info] Automated version update PR merged for module '" + module['name'] \
                                  + "'. PR: " + pull_request.html_url
                    print(log_message)
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
            print("[Error] Dependency update PR checks have failed for '" + module_name + "'")
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
    if module['name'] == 'ballerina-distribution':
        current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_RELEASED
        current_level_modules[index][MODULE_STATUS] = MODULE_STATUS_COMPLETED
        status_completed_modules += 1
    elif module[MODULE_CONCLUSION] == MODULE_CONCLUSION_BUILD_PENDING:
        for build_check in repo.get_commit(sha=sha).get_check_runs():
            build_check_found = True
            # Ignore codecov checks temporarily due to bug
            if not build_check.name.startswith('codecov') and not build_check.name.startswith('SonarCloud') and 'graalvm' not in build_check.name:
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
                print("[Error] Dependency update PR merge build checks have failed for '" + module_name + "'")
                for name, html_url in zip(failed_build_name, failed_build_html):
                    print("[" + module_name + "] Build check '" + name + "' failed for " + html_url)
                status_completed_modules += 1
    else:
        # Already successful and merged
        current_level_modules[index][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_SUCCESS

    if current_level_modules[index][MODULE_CONCLUSION] == MODULE_CONCLUSION_BUILD_SUCCESS:
        try:
            packages_url = 'https://api.github.com/orgs/' + constants.BALLERINA_ORG_NAME + '/packages/maven/' \
                           + module['group_id'] + '.' + module['artifact_id'] + '/versions'
            packages_list_string = utils.open_url(packages_url).read()
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
    updated_properties_file = get_updated_properties_file(module['name'], current_level, properties_file)

    update = utils.commit_file(module['name'], constants.GRADLE_PROPERTIES_FILE, updated_properties_file,
                               constants.DEPENDENCY_UPDATE_BRANCH, COMMIT_MESSAGE)[0]

    if update:
        print("[Info] Update lang dependency in module '" + module['name'] + "'")
        create_pull_request(idx, repo)
    else:
        current_level_modules[idx][MODULE_STATUS] = MODULE_STATUS_IN_PROGRESS
        current_level_modules[idx][MODULE_CONCLUSION] = MODULE_CONCLUSION_BUILD_SUCCESS
        current_level_modules[idx][MODULE_CREATED_PR] = None

        pulls = repo.get_pulls(state='closed')
        sha_of_lang = lang_version.split('-')[-1]

        if skip_lang_update:
            current_level_modules[idx][MODULE_CREATED_PR] = pulls[0]
        else:
            for pull in pulls:
                if sha_of_lang in pull.title:
                    current_level_modules[idx][MODULE_CREATED_PR] = pull
                    break


def get_updated_properties_file(module_name, current_level, properties_file):
    updated_properties_file = ''

    split_lang_version = lang_version.split('-')
    if len(split_lang_version) > 3:
        processed_lang_version = split_lang_version[1] + split_lang_version[2]
    else:
        processed_lang_version = split_lang_version[1]

    for line in properties_file.splitlines():
        if line.startswith(constants.LANG_VERSION_KEY):
            if skip_lang_update.lower() == 'false':
                current_version = line.split('=')[-1]

                split_current_version = current_version.split('-')

                if len(split_current_version) == 5:
                    # Prerelease version
                    processed_current_version = split_current_version[2] + split_current_version[3]

                    if processed_current_version < processed_lang_version:
                        print("[Info] Updating the lang version in module: '" + module_name + "'")
                        updated_properties_file += constants.LANG_VERSION_KEY + '=' + lang_version + '\n'
                    else:
                        updated_properties_file += line + '\n'
                elif len(split_current_version) == 4:
                    processed_current_version = split_current_version[1] + split_current_version[2]
                    if processed_current_version < processed_lang_version:
                        print("[Info] Updating the lang version in module: '" + module_name + "'")
                        updated_properties_file += constants.LANG_VERSION_KEY + '=' + lang_version + '\n'
                    else:
                        updated_properties_file += line + '\n'
                else:
                    # Stable dependency & SNAPSHOT
                    print("[Info] Updating the lang version in module: '" + module_name + "'")
                    updated_properties_file += constants.LANG_VERSION_KEY + '=' + lang_version + '\n'
            else:
                updated_properties_file += line + '\n'
        else:
            key_found = False
            possible_dependency_modules = list(filter(lambda s: s['level'] < current_level, all_modules))

            for possible_dependency in possible_dependency_modules:
                if line.startswith(possible_dependency['version_key']):
                    updated_line = possible_dependency['version_key'] + '=' \
                                   + possible_dependency[MODULE_TIMESTAMPED_VERSION]
                    updated_properties_file += updated_line + '\n'
                    key_found = True
                    break
            if not key_found:
                updated_properties_file += line + '\n'

    return updated_properties_file


def create_pull_request(idx: int, repo):
    module = current_level_modules[idx]
    pulls = repo.get_pulls(state='open')
    pr_exists = False
    created_pr = ''

    sha_of_lang = lang_version.split('-')[-1]

    for pull in pulls:
        if pull.head.ref == constants.DEPENDENCY_UPDATE_BRANCH:
            pr_exists = True
            created_pr = pull
            pull.edit(
                title=pull.title.rsplit('-', 1)[0] + '-' + sha_of_lang + ')',
                body=pull.body.rsplit('-', 1)[0] + '-' + sha_of_lang + '` and relevant extensions.'
            )
            print("[Info] Automated version update PR found for module '" + module['name'] + "'. PR: " + pull.html_url)
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
                head=constants.DEPENDENCY_UPDATE_BRANCH,
                base=repo.default_branch
            )
            log_message = "[Info] Automated version update PR created for module '" + module['name'] \
                          + "'. PR: " + created_pr.html_url
            print(log_message)
        except Exception as e:
            print("[Error] Error occurred while creating pull request for module '" + module['name'] + "'.", e)
            sys.exit(1)

    try:
        utils.approve_pr(module, auto_merge_pull_requests, created_pr.number)
    except Exception as e:
        print("[Error] Error occurred while approving dependency PR for module '" + module['name'] + "'", e)

    current_level_modules[idx][MODULE_CREATED_PR] = created_pr
    current_level_modules[idx][MODULE_STATUS] = MODULE_STATUS_IN_PROGRESS
    current_level_modules[idx][MODULE_CONCLUSION] = MODULE_CONCLUSION_PR_PENDING


main()
