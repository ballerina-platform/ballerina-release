import os
import sys
import time

from github import Github, InputGitAuthor, GithubException

import constants
import notify_chat
import utils

PULL_REQUEST_TITLE = '[Automated] Bump Ballerina Lang version'
COMMIT_MESSAGE_PREFIX = '[Automated] Update ballerina lang to '

SLEEP_INTERVAL = 30 # 30s
MAX_WAIT_CYCLES = 180 # script timeout is 90 minutes

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
ballerina_bot_email = os.environ[constants.ENV_BALLERINA_BOT_EMAIL]
ballerina_reviewer_bot_token = os.environ[constants.ENV_BALLERINA_REVIEWER_BOT_TOKEN]
github = Github(ballerina_bot_token)

def main():
    branch_name = sys.argv[1]
    lang_version = sys.argv[2]
    update_lang_version(branch_name, lang_version)

def update_lang_version(branch_name, lang_version):
    dist_repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/ballerina-distribution', branch_name)
    properties_content = dist_repo.get_contents(constants.GRADLE_PROPERTIES_FILE)
    properties_content = properties_content.decoded_content.decode(constants.ENCODING)

    synced = False
    updated_properties_file = ''
    module = {'name': 'ballerina-distribution', 'auto_merge': True}
    for line in properties_content.splitlines():
        if line.startswith('ballerinaLangVersion'):
            if line.split('=')[1] == lang_version:
                print("[Info] lang version is already synced in " + branch_name + " branch")
                Synced = True
                break
            else:
                updated_properties_file += 'ballerinaLangVersion' + '=' + lang_version + '\n'
        else:
            updated_properties_file += line + '\n'

    if not synced:
        committed = commit_file(dist_repo, constants.GRADLE_PROPERTIES_FILE, updated_properties_file,
                   branch_name, COMMIT_MESSAGE_PREFIX + lang_version)

        print("[Info] Update lang version in " + branch_name + " branch")
        if committed:
            pr = create_pull_request(dist_repo, branch_name)
            utils.approve_pr(module, 'TRUE', pr.number)
            ref = dist_repo.get_git_ref('heads/' + branch_name + "_temp")
            pending = True
            wait_cycles = 0
            while pending:
                if wait_cycles < MAX_WAIT_CYCLES:
                    time.sleep(SLEEP_INTERVAL)
                    pending, passing, failing_pr_checks = check_pending_pr_checks(dist_repo, pr)
                    if not pending:
                        if len(failing_pr_checks) > 0:
                            passing = all(check.startswith('codecov') for check in failing_pr_checks)
                        if passing:
                            if(pr.mergeable_state != 'dirty'):
                                try:
                                    pr.merge()
                                    ref.delete()
                                    log_message = "[Info] Automated lang version update PR merged. PR: " + pr.html_url
                                    print(log_message)
                                except Exception as e:
                                    print("[Error] Error occurred while merging version update PR " , e)
                            else:
                                notify_chat.send_message("[Info] Automated ballerina-distribution version update PR is unmerged due to conflicts." + "\n" +\
                                        "Please visit <" + pr.html_url + "|the build page> for more information")
                        else:
                            notify_chat.send_message("[Info] Automated ballerina-distribution version update PR has failed checks." + "\n" +\
                                "Please visit <" + pr.html_url + "|the build page> for more information")
                            pr.edit(state = 'closed')
                            ref.delete()
                    else:
                        wait_cycles += 1
                else:
                    notify_chat.send_message("[Info] Automated ballerina-distribution version update PR is unmerged due to pr checks timeout." + "\n" +\
                        "Please visit <" + pr.html_url + "|the build page> for more information")
                    break
    else:
        print("[Info] Lang version is already synced")

def commit_file(repo, file_path, updated_file_content, branch_name, commit_message):
    try:
        temp_branch = branch_name + "_temp"
        author = InputGitAuthor(ballerina_bot_username, ballerina_bot_email)
        pulls = repo.get_pulls(state='open')
        for pull in pulls:
            if (pull.head.ref == temp_branch):
                print( "[info] " + branch_name + " has a pull request from " + temp_branch)
                pull.edit(state = 'closed')

        branches = repo.get_branches()
        for branch in branches:
            if branch.name == temp_branch:
                ref = repo.get_git_ref('heads/' + temp_branch)
                ref.delete()
                break

        for branch in branches:
            if branch.name == branch_name:
                src_branch = branch
                break

        repo.create_git_ref(ref='refs/heads/' + temp_branch, sha=src_branch.commit.sha)

        # commit the changes to temporary branch
        repo.update_file(
                file_path,
                commit_message,
                updated_file_content,
                repo.get_contents(file_path).sha,
                branch=temp_branch,
                author=author
            )
        return True
    except GithubException as e:
        raise e

def create_pull_request(repo, branch_name):
    try:
        pull_request_title = PULL_REQUEST_TITLE
        created_pr = repo.create_pull(
                        title=pull_request_title,
                        body='[Automated] Update Ballerina Lang Version',
                        head=branch_name + "_temp",
                        base=branch_name
                    )
        log_message = "[Info] Automated lang version bump PR created for branch '" + branch_name \
                      + "'. PR: " + created_pr.html_url
        print(log_message)
        return created_pr
    except Exception as e:
        print("[Error] Error occurred while creating pull request for branch '" + branch_name + "'.", e)
        sys.exit(1)

def check_pending_pr_checks(repo, pr):
    print("[Info] Checking the status of the lang version bump PR ")
    passing = True
    pending = False

    failed_pr_checks = []
    pull_request = repo.get_pull(pr.number)
    sha = pull_request.head.sha
    for pr_check in repo.get_commit(sha=sha).get_check_runs():
        if pr_check.status != 'completed':
            pending = True
            break
        elif pr_check.conclusion == 'success':
            continue
        else:
            failed_pr_checks.append(pr_check.name)
            passing = False
    return pending, passing, failed_pr_checks

main()
