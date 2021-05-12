import os
import sys
import time

from github import Github

import constants
import utils

CONNECTOR_CREATED_PR = 'created_pr'
CONNECTOR_STATUS = 'status'
CONNECTOR_STATUS_IN_PROGRESS = 'in_progress'
CONNECTOR_STATUS_COMPLETED = 'completed'

CONNECTOR_CONCLUSION = 'conclusion'
CONNECTOR_CONCLUSION_PR_CHECK_FAILURE = 'pr_check_failure'
CONNECTOR_CONCLUSION_PR_MERGE_FAILURE = 'merge_failure'
CONNECTOR_CONCLUSION_PR_MERGE_SUCCESS = 'merge_success'
CONNECTOR_CONCLUSION_PR_NOT_MERGED = 'pr_not_merged'

COMMIT_MESSAGE_PREFIX = '[Automated] Update ballerina lang to '
PULL_REQUEST_BODY_PREFIX = 'Update ballerina lang version to `'
PULL_REQUEST_TITLE = '[Automated] Update Ballerina Lang Version ('
AUTO_MERGE_PULL_REQUEST_TITLE = '[AUTO MERGE] Ballerina Lang Version ('

SLEEP_INTERVAL = 30  # 30s
MAX_WAIT_CYCLES = 120  # Script timeout is 1h

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]

ballerina_version = sys.argv[1]
auto_merge_pull_requests = sys.argv[2]

event_type = 'workflow_dispatch'
if len(sys.argv) > 3:
    event_type = sys.argv[3]

github = Github(ballerina_bot_token)

connectors = []


def main():
    global connectors
    global auto_merge_pull_requests

    print('Workflow started with Ballerina Lang version : ' + ballerina_version)

    try:
        connector_file = utils.read_json_file(constants.CONNECTORS_FILE)
        connectors = connector_file['modules']
    except Exception as e:
        print('[Error] Error while loading connectors list ', e)
        sys.exit(1)

    print("Workflow invoked of type '" + event_type + "'")
    if event_type == 'repository_dispatch' and not connector_file['auto_bump']:
        print("Workflow invoked with 'repository dispatch' type, exiting script as 'auto_bump' flag connector_list.json is false.")
        return

    for index, connector in enumerate(connectors):
        print("[Info] Check lang dependency in connector '" + connector['name'] + "'")
        update_connector(index)

    if auto_merge_pull_requests.lower() == 'true':
        total_connectors = len(connectors)

        wait_cycles = 0
        status_completed_connectors = 0

        while status_completed_connectors != total_connectors:
            for index, connector in enumerate(connectors):
                if connector[CONNECTOR_STATUS] == CONNECTOR_STATUS_IN_PROGRESS:
                    check_pending_pr_checks(index)
                else:
                    status_completed_connectors += 1

            if wait_cycles < MAX_WAIT_CYCLES:
                time.sleep(SLEEP_INTERVAL)
                wait_cycles = wait_cycles + 1
            else:
                # Force stop script with all in progress connector printed
                print('Dependency bump script timed out. Following connectors are in pending state')
                for connector in connectors:
                    if connector[CONNECTOR_STATUS] == CONNECTOR_STATUS_IN_PROGRESS:
                        print(connector['name'])
                sys.exit(1)

        connector_release_failure = False
        pr_checks_failed_modules = list(
            filter(lambda s: s[CONNECTOR_CONCLUSION] == CONNECTOR_CONCLUSION_PR_CHECK_FAILURE, connectors))
        if len(pr_checks_failed_modules) != 0:
            connector_release_failure = True
            print('Following modules dependency PRs have failed checks...')
            for module in pr_checks_failed_modules:
                print(module['name'])

        pr_merged_failed_modules = list(
            filter(lambda s: s[CONNECTOR_CONCLUSION] == CONNECTOR_CONCLUSION_PR_MERGE_FAILURE, connectors))
        if len(pr_merged_failed_modules) != 0:
            connector_release_failure = True
            print('Following modules dependency PRs could not be merged...')
            for module in pr_merged_failed_modules:
                print(module['name'])

        if connector_release_failure:
            sys.exit(1)

    print('Successfully bumped ballerina version in connectors')


def update_connector(index: int):
    global connectors

    connector = connectors[index]
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + connector['name'])

    properties_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE)
    properties_file = properties_file.decoded_content.decode(constants.ENCODING)

    updated_properties_file = ''
    for line in properties_file.splitlines():
        if line.startswith(constants.LANG_VERSION_KEY):
            updated_properties_file += constants.LANG_VERSION_KEY + '=' + ballerina_version + '\n'
        else:
            updated_properties_file += line + '\n'

    update = utils.commit_file(connector['name'], constants.GRADLE_PROPERTIES_FILE, updated_properties_file,
                               constants.DEPENDENCY_UPDATE_BRANCH,
                               COMMIT_MESSAGE_PREFIX + ballerina_version)

    if update:
        print("[Info] Update lang dependency in connector '" + connector['name'] + "'")
        pr = create_pull_request(index, repo)
        connectors[index][CONNECTOR_STATUS] = CONNECTOR_STATUS_IN_PROGRESS
        connectors[index][CONNECTOR_CREATED_PR] = pr
    else:
        connectors[index][CONNECTOR_STATUS] = CONNECTOR_STATUS_COMPLETED


def create_pull_request(idx: int, repo):
    global connectors

    connector = connectors[idx]
    pulls = repo.get_pulls(state='open')
    pr_exists = False
    created_pr = ''

    sha_of_lang = ballerina_version.split('-')[-1]

    for pull in pulls:
        if pull.head.ref == constants.DEPENDENCY_UPDATE_BRANCH:
            pr_exists = True
            created_pr = pull
            pull.edit(
                title=pull.title.rsplit('-', 1)[0] + '-' + sha_of_lang + ')',
                body=pull.body.rsplit('-', 1)[0] + '-' + sha_of_lang + '`.'
            )
            print("[Info] Automated version bump PR found for connector '" + connector[
                'name'] + "'. PR: " + pull.html_url)
            break

    if not pr_exists:
        try:
            pull_request_title = PULL_REQUEST_TITLE
            if (auto_merge_pull_requests.lower() == 'true') & connector['auto_merge']:
                pull_request_title = AUTO_MERGE_PULL_REQUEST_TITLE
            pull_request_title = pull_request_title + ballerina_version + ')'

            created_pr = repo.create_pull(
                title=pull_request_title,
                body=PULL_REQUEST_BODY_PREFIX + ballerina_version + '`.',
                head=constants.DEPENDENCY_UPDATE_BRANCH,
                base=repo.default_branch
            )
            log_message = "[Info] Automated version bump PR created for connector '" + connector['name'] \
                          + "'. PR: " + created_pr.html_url
            print(log_message)
        except Exception as e:
            print("[Error] Error occurred while creating pull request for connector '" + connector['name'] + "'.", e)
            sys.exit(1)

        try:
            utils.approve_pr(connector, auto_merge_pull_requests, created_pr.number)
        except Exception as e:
            print("[Error] Error occurred while approving dependency PR for connector '" + connector['name'] + "'", e)
    return created_pr


def check_pending_pr_checks(index: int):
    global connectors

    connector = connectors[index]

    print("[Info] Checking the status of the dependency bump PR in connector '" + connector['name'] + "'")

    passing = True
    pending = False
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + connector['name'])

    failed_pr_checks = []
    pull_request = repo.get_pull(connector[CONNECTOR_CREATED_PR].number)
    sha = pull_request.head.sha
    for pr_check in repo.get_commit(sha=sha).get_check_runs():
        # Ignore codecov checks temporarily due to bug
        if not pr_check.name.startswith('codecov'):
            if pr_check.status != 'completed':
                pending = True
                break
            elif pr_check.conclusion == 'success':
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
            if connector['auto_merge'] & ('AUTO MERGE' in pull_request.title):
                try:
                    pull_request.merge()
                    log_message = "[Info] Automated version bump PR merged for connector '" + connector['name'] \
                                  + "'. PR: " + pull_request.html_url
                    print(log_message)
                    connectors[index][CONNECTOR_STATUS] = CONNECTOR_STATUS_COMPLETED
                    connectors[index][CONNECTOR_CONCLUSION] = CONNECTOR_CONCLUSION_PR_MERGE_SUCCESS
                except Exception as e:
                    print("[Error] Error occurred while merging dependency PR for connector '" +
                          connectors[index]['name'] + "'", e)
                    connectors[index][CONNECTOR_STATUS] = CONNECTOR_STATUS_COMPLETED
                    connectors[index][CONNECTOR_CONCLUSION] = CONNECTOR_CONCLUSION_PR_MERGE_FAILURE
            else:
                connectors[index][CONNECTOR_STATUS] = CONNECTOR_STATUS_COMPLETED
                connectors[index][CONNECTOR_CONCLUSION] = CONNECTOR_CONCLUSION_PR_NOT_MERGED
        else:
            connectors[index][CONNECTOR_STATUS] = CONNECTOR_STATUS_COMPLETED
            connectors[index][CONNECTOR_CONCLUSION] = CONNECTOR_CONCLUSION_PR_CHECK_FAILURE
            connector_name = connector['name']
            print("[Error] Dependency bump PR checks have failed for '" + connector_name + "'")
            for check in failed_pr_checks:
                print("[" + connector_name + "] PR check '" + check["name"] + "' failed for " + check["html_url"])


main()
