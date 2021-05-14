from json import dumps
import os

from github import Github, GithubException

from httplib2 import Http

import constants
import utils

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
build_chat_id = os.environ[constants.ENV_BALLERINA_BUILD_CHAT_ID]
build_chat_key = os.environ[constants.ENV_BALLERINA_BUILD_CHAT_KEY]
build_chat_token = os.environ[constants.ENV_BALLERINA_BUILD_CHAT_TOKEN]

github = Github(ballerina_bot_token)

older_version = []
updated_version = []


def send_message(message):
    """Hangouts Chat incoming webhook quickstart."""
    url = 'https://chat.googleapis.com/v1/spaces/'+build_chat_id+'/messages?key='+build_chat_key+'&token='+build_chat_token
    bot_message = {
        'text': message}

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )


def remove_statement_changes():
    global older_version
    global updated_version
    for i in range(min(2, len(older_version))):
        if any(x in older_version[0] for x in ["`ballerina-distribution`", "`ballerina-lang`"]):
            del older_version[0]
            del updated_version[0]


def create_message():
    global older_version
    global updated_version

    color_order = {"brightgreen":0, "yellow":1, "red":2}
    chat_message = ""

    for i in range(len(older_version)):
        old_row = older_version[i].split("|")[1:-1]
        updated_row = updated_version[i].split("|")[1:-1]

        if old_row[2] != updated_row[2]:
            old_color = old_row[2].split("-")[2].split(")")[0]
            updated_color = updated_row[2].split("-")[2].split(")")[0]
            if(color_order[updated_color]>color_order[old_color]):
                if not chat_message:
                    chat_message = "Reminder on the following modules dependency update..." + "\n"
                chat_message += old_row[2].split("(")[2][:-2] + "\n"

    if chat_message:
        print(chat_message)
        send_message(chat_message)


def notify_failing_pr(failed_modules):
    chat_message = "Following modules dependency PRs have failed checks..." + "\n"
    for module in failed_modules:
        pr_number = check_pending_pr_checks(module["name"])
        pending_pr_link = "https://github.com/ballerina-platform/" + module["name"] + "/pull/" + str(
            pr_number)
        chat_message += pending_pr_link + "\n"

    send_message(chat_message)


def check_pending_pr_checks(module_name):
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    pulls = repo.get_pulls(state="open")

    for pull in pulls:
        if pull.head.ref == constants.DEPENDENCY_UPDATE_BRANCH:
            return pull.number
    return None


def send_chat(commit):
    global older_version
    global updated_version
    repo = github.get_repo("ballerina-platform" + '/' + "ballerina-release")

    diff_string = utils.open_url(
        "https://github.com/ballerina-platform/ballerina-release/commit/" + commit + ".diff").read().decode("utf-8")

    for line in diff_string.splitlines():
        if line.startswith("-"):
            older_version.append(line[1:])
        elif line.startswith("+"):
            updated_version.append(line[1:])

    older_version = older_version[1:]
    updated_version = updated_version[1:]

    remove_statement_changes()

    create_message()
