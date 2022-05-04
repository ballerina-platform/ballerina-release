import os
import sys
import time

from github import Github
from datetime import date

import constants
import notify_chat

PULL_REQUEST_TITLE = '[Automated] Merge patch branch with the master'

SLEEP_INTERVAL = 30 # 30s
MAX_WAIT_CYCLES = 180 # script timeout is 90 minutes

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
ballerina_reviewer_bot_token = os.environ[constants.ENV_BALLERINA_REVIEWER_BOT_TOKEN]
github = Github(ballerina_bot_token)

def main():
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + 'ballerina-lang')
    branches = repo.get_branches()
    temp_branch = 'sync-2201.1.x-' + date.today().strftime("%d-%m-%Y")

    for branch in branches:
        if (branch.name == '2201.1.x'):
            patch_branch = branch
            break

    # Check whether master branch already has an unmerged PR from temporary branch, delete if exists
    pulls = repo.get_pulls(state='open')
    for pull in pulls:
        if (pull.head.ref == temp_branch):
            print ("Master branch already has an open pull request from " + temp_branch)
            pull.edit(state = 'closed')
            break

    # if temporary branch exists, delete it
    for branch in branches:
        if branch.name == temp_branch:
            ref = repo.get_git_ref('heads/' + temp_branch)
            ref.delete()
            break

    # create the temporary branch from patch branch
    repo.create_git_ref(ref='refs/heads/' + temp_branch, sha=patch_branch.commit.sha)
    ref = repo.get_git_ref('heads/' + temp_branch)

    pr = create_pull_request(repo, temp_branch)
    time.sleep(10)

    pending = True
    wait_cycles = 0
    if(pr.mergeable_state != 'dirty'):
        while pending:
            if wait_cycles < MAX_WAIT_CYCLES:
                time.sleep(SLEEP_INTERVAL)
                pending, passing, failing_pr_checks = check_pending_pr_checks(repo, pr)
                if not pending:
                    if len(failing_pr_checks) > 0:
                        passing = all(check.startswith('codecov') for check in failing_pr_checks)
                    if passing:
                        try:
                            pr.merge()
                            ref.delete()
                            log_message = "[Info] Automated master update PR merged. PR: " + pr.html_url
                            print(log_message)
                        except Exception as e:
                            print("[Error] Error occurred while merging master update PR " , e)
                    else:
                        notify_chat.send_message("[Info] Automated ballerina-lang master update PR has failed checks." + "\n" +\
                         "Please visit <" + pr.html_url + "|the build page> for more information")
                        pr.edit(state = 'closed')
                        ref.delete()
                else:
                    wait_cycles += 1
            else:
                notify_chat.send_message("[Info] Automated ballerina-lang master update PR is unmerged due to pr checks timeout." + "\n" +\
                 "Please visit <" + pr.html_url + "|the build page> for more information")
                break
    else:
        notify_chat.send_message("[Info] Automated ballerina-lang master update PR is unmerged due to conflicts with the master." + "\n" +\
                "Please visit <" + pr.html_url + "|the build page> for more information")

def create_pull_request(repo, temp_branch):
    try:
        pull_request_title = PULL_REQUEST_TITLE
        created_pr = repo.create_pull(
            title=pull_request_title,
            body='[Automated] Daily syncing of patch branch content with the master',
            head=temp_branch,
            base=repo.default_branch
        )
        log_message = "[Info] Automated PR created for ballerina-lang repo at " + created_pr.html_url
        print(log_message)
    except Exception as e:
        print("[Error] Error occurred while creating pull request ", e)
        sys.exit(1)

    try:
        approve_pr(created_pr.number)
    except Exception as e:
        print("[Error] Error occurred while approving the PR ", e)
    return created_pr

def approve_pr(pr_number):
    time.sleep(5)
    r_github = Github(ballerina_reviewer_bot_token)
    repo = r_github.get_repo(constants.BALLERINA_ORG_NAME + '/ballerina-lang')
    pr = repo.get_pull(pr_number)
    try:
        pr.create_review(event='APPROVE')
        print(
            "[Info] Automated master update PR approved. PR: " + pr.html_url)
    except Exception as e:
        raise e

def check_pending_pr_checks(repo, pr):
    print("[Info] Checking the status of the dependency master syncing PR ")
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
