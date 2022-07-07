import os
import sys
import time

from github import Github, InputGitAuthor, GithubException
import github

import constants
import utils

SLEEP_INTERVAL = 30 # 30s
MAX_WAIT_CYCLES = 180 # script timeout is 90 minutes

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
ballerina_bot_email = os.environ[constants.ENV_BALLERINA_BOT_EMAIL]
ballerina_reviewer_bot_token = os.environ[constants.ENV_BALLERINA_REVIEWER_BOT_TOKEN]

ballerina_org_name="ballerina-platform"
github = Github(ballerina_bot_token)

def main():
     
    dist_repo = github.get_repo(ballerina_org_name + '/ballerina-release')
    build_time_data_branch=dist_repo.get_branch('build-time-data')
    try:
        dist_repo.get_git_ref('heads/temp-build-time-data').delete()
    except  GithubException:
        print("Temporary branch does not exist")
    dist_repo.create_git_ref(ref='refs/heads/temp-build-time-data' , sha=build_time_data_branch.commit.sha)
    with open("build-time-data/hello_world.json") as f:
        hello_world_json_content = f.read()
    with open("build-time-data/hello_world_service.json") as f:
        hello_world_service_json_content = f.read()
    with open("build-time-data/nballerina.json") as f:
        nballerina_json_content = f.read()

    author = InputGitAuthor(ballerina_bot_username, ballerina_bot_email)

    try:
        dist_repo.update_file(
                        "build-time-data/hello_world.json",
                        "Add hello_world.json",
                        hello_world_json_content,
                        dist_repo.get_contents("build-time-data/hello_world.json","build-time-data").sha,
                        branch="temp-build-time-data",
                        author=author
                    )
        dist_repo.update_file(
                        "build-time-data/hello_world_service.json",
                        "Add hello_world_service.json",
                        hello_world_service_json_content,
                        dist_repo.get_contents("build-time-data/hello_world_service.json","build-time-data").sha,
                        branch="temp-build-time-data",
                        author=author
                    )

        dist_repo.update_file(
                        "build-time-data/nballerina.json",
                        "Add nballerina.json",
                        nballerina_json_content,
                        dist_repo.get_contents("build-time-data/nballerina.json","build-time-data").sha,
                        branch="temp-build-time-data",
                        author=author
                    )
    except Exception:

        dist_repo.create_file(
                        "build-time-data/hello_world.json",
                        "Add hello_world.json",
                        hello_world_json_content,
                        branch="temp-build-time-data",
                        author=author
                    )
        dist_repo.create_file(
                        "build-time-data/hello_world_service.json",
                        "Add hello_world_service.json",
                        hello_world_service_json_content,
                        branch="temp-build-time-data",
                        author=author
                    )

        dist_repo.create_file(
                        "build-time-data/nballerina.json",
                        "Add nballerina.json",
                        nballerina_json_content,
                        branch="temp-build-time-data",
                        author=author
                    )


    time.sleep(5)
    pr=create_pull_request(dist_repo)
    module = {'name': 'ballerina-release', 'auto_merge': True}
    utils.approve_pr(module, 'TRUE', pr.number)
    ref = dist_repo.get_git_ref('heads/temp-build-time-data')
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
                            log_message = "[Info] Automated build-time-stats generation PR is merged. PR: " + pr.html_url
                            print(log_message)
                        except Exception as e:
                            print("[Error] Error occurred while merging automated build time stats generation PR " , e)
                    else:
                        print("[Info] Automated build-time-stats generation PR is unmerged due to conflicts." + "\n" +\
                                "Please visit <" + pr.html_url + "|the build page> for more information")
                else:
                    print("[Info] Automated build-time-stats generation PR has failed checks." + "\n" +\
                        "Please visit <" + pr.html_url + "|the build page> for more information")
                    pr.edit(state = 'closed')
                    ref.delete()
            else:
                wait_cycles += 1
        else:
            print("[Info] Automated build-time-stats generation PR is unmerged due to pr checks timeout." + "\n" +\
                "Please visit <" + pr.html_url + "|the build page> for more information")
            break


def create_pull_request(repo):
    try:
        pull_request_title = "[Automated] Add build time statistics files"
        created_pr = repo.create_pull(
                        title=pull_request_title,
                        body='[Automated] Add build time statistics files',
                        head="temp-build-time-data",
                        base="build-time-data"
                    )
        return created_pr
    except Exception as e:
        print("[Error] Error occurred while creating pull request for branch build-time-data.", e)
        sys.exit(1)


def check_pending_pr_checks(repo, pr):
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
