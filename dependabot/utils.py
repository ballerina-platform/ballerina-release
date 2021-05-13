import json
import os
import time
import urllib.request

from github import Github, InputGitAuthor, GithubException
from retry import retry

import constants

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
ballerina_bot_email = os.environ[constants.ENV_BALLERINA_BOT_EMAIL]
ballerina_reviewer_bot_token = os.environ[constants.ENV_BALLERINA_REVIEWER_BOT_TOKEN]

github = Github(ballerina_bot_token)


def read_json_file(file_path):
    try:
        with open(file_path) as f:
            module_list = json.load(f)
    except Exception as e:
        raise e

    return module_list


def write_json_file(file_path, file_content):
    try:
        with open(file_path, 'w') as json_file:
            json_file.seek(0)
            json.dump(file_content, json_file, indent=4)
            json_file.truncate()
    except Exception as e:
        raise e


@retry(
    urllib.error.URLError,
    tries=constants.HTTP_REQUEST_RETRIES,
    delay=constants.HTTP_REQUEST_DELAY_IN_SECONDS,
    backoff=constants.HTTP_REQUEST_DELAY_MULTIPLIER
)
def open_url(url):
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github.v3+json")
    request.add_header("Authorization", "Bearer " + ballerina_bot_token)

    return urllib.request.urlopen(request)


def get_latest_lang_version():
    try:
        version_string = open_url(
            "https://api.github.com/orgs/ballerina-platform/packages/maven/org.ballerinalang.jballerina-debugger-integration-test/versions"
        ).read()
    except Exception as e:
        raise e

    versions_list = json.loads(version_string)
    latest_version = versions_list[0]['name']

    extensions_file = read_json_file(constants.EXTENSIONS_FILE)

    if extensions_file['lang_version_substring'] != "":
        for version in versions_list:
            version_name = version['name']
            if extensions_file['lang_version_substring'] in version_name:
                latest_version = version_name
                break
    return latest_version


def commit_file(repository_name, file_path, updated_file_content, commit_branch, commit_message):
    try:
        author = InputGitAuthor(ballerina_bot_username, ballerina_bot_email)

        repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + repository_name)

        remote_file = repo.get_contents(file_path)
        remote_file_contents = remote_file.decoded_content.decode(constants.ENCODING)

        try:
            remote_file_in_pr_branch = repo.get_contents(file_path, commit_branch)
            remote_file_in_pr_branch = remote_file_in_pr_branch.decoded_content.decode(constants.ENCODING)
        except GithubException:
            remote_file_in_pr_branch = ""

        if updated_file_content == remote_file_contents:
            return False
        elif updated_file_content == remote_file_in_pr_branch:
            return True
        else:
            base = repo.get_branch(repo.default_branch)
            branch = commit_branch
            try:
                ref = f"refs/heads/" + branch
                repo.create_git_ref(ref=ref, sha=base.commit.sha)
            except GithubException:
                print("[Info] Unmerged '" + commit_branch + "' branch existed in '" + repository_name + "'")
                branch = commit_branch + '_tmp'
                ref = f"refs/heads/" + branch
                try:
                    repo.create_git_ref(ref=ref, sha=base.commit.sha)
                except GithubException as e:
                    print("[Info] Deleting '" + commit_branch + "' tmp branch existed in '" + repository_name + "'")
                    if e.status == 422:  # already exist
                        repo.get_git_ref("heads/" + branch).delete()
                        repo.create_git_ref(ref=ref, sha=base.commit.sha)
            update = repo.update_file(
                file_path,
                commit_message,
                updated_file_content,
                remote_file.sha,
                branch=branch,
                author=author
            )
            if not branch == commit_branch:
                update_branch = repo.get_git_ref("heads/" + commit_branch)
                update_branch.edit(update["commit"].sha, force=True)
                repo.get_git_ref("heads/" + branch).delete()
            return True
    except GithubException as e:
        raise e


def open_pr_and_merge(repository_name, title, body, head_branch):
    try:
        repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + repository_name)

        created_pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base='master'
        )

        # To stop intermittent failures due to API sync
        time.sleep(5)

        r_github = Github(ballerina_reviewer_bot_token)
        repo = r_github.get_repo(constants.BALLERINA_ORG_NAME + '/' + repository_name)
        pr = repo.get_pull(created_pr.number)
        pr.create_review(event='APPROVE')

        created_pr.merge()
    except Exception as e:
        raise e


def approve_pr(module, auto_merge_pull_requests, pr_number):
    if (auto_merge_pull_requests.lower() == 'true') & module['auto_merge']:

        # To stop intermittent failures due to API sync
        time.sleep(5)

        r_github = Github(ballerina_reviewer_bot_token)
        repo = r_github.get_repo(constants.BALLERINA_ORG_NAME + '/' + module['name'])
        pr = repo.get_pull(pr_number)
        try:
            pr.create_review(event='APPROVE')
            print(
                "[Info] Automated version bump PR approved for module '" + module['name'] + "'. PR: " + pr.html_url)
        except Exception as e:
            raise e
