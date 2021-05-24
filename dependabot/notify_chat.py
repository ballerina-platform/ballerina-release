import os
from json import dumps

from httplib2 import Http

import constants
import utils

older_version = []
updated_version = []


def send_message(message):
    build_chat_id = os.environ[constants.ENV_BALLERINA_BUILD_CHAT_ID]
    build_chat_key = os.environ[constants.ENV_BALLERINA_BUILD_CHAT_KEY]
    build_chat_token = os.environ[constants.ENV_BALLERINA_BUILD_CHAT_TOKEN]

    url = 'https://chat.googleapis.com/v1/spaces/' + build_chat_id + \
          '/messages?key=' + build_chat_key + '&token=' + build_chat_token
    bot_message = {
        'text': message}

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )


def remove_statement_changes():
    global older_version
    global updated_version
    for i in range(min(2, len(older_version))):
        if any(x in older_version[0] for x in ["<code>ballerina-distribution</code>", "<code>ballerina-lang</code>"]):
            del older_version[0]
            del updated_version[0]


def create_message():
    global older_version
    global updated_version

    color_order = {"brightgreen": 0, "yellow": 1, "red": 2}
    chat_message = ""

    for i in range(len(older_version)):
        old_row = older_version[i].split("|")[2:-1]
        updated_row = updated_version[i].split("|")[2:-1]

        if old_row[2] != updated_row[2]:
            old_color = old_row[2].split("-")[2].split(")")[0].split("?")[0]
            updated_color = updated_row[2].split("-")[2].split(")")[0].split("?")[0]
            pending_pr = updated_row[3].split("[")[1].split("]")[0]
            if color_order[updated_color] > color_order[old_color] and pending_pr:
                chat_message = "Reminder on the following modules dependency update..." + "\n"
                chat_message += old_row[2].split("(")[2][:-2] + "\n"
                break

    return chat_message


def notify_lag_update(commit):
    global older_version
    global updated_version

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

    chat_message = create_message()

    if chat_message:
        print(chat_message)
        send_message(chat_message)


create_message()