import io
import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
from PIL import Image
from github import Github, GithubException

import constants
import notify_chat
import utils

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]

README_FILE = "README.md"

github = Github(ballerina_bot_token)

all_modules = []
modules_with_no_lag = 0

is_distribution_lagging = False
distribution_lag_statement = ''
lagging_modules_level = 0
lag_reminder_modules = []

MODULE_NAME = "name"
MODULE_BUILD_ACTION_FILE = "build_action_file"
MODULE_PULL_REQUEST = "pull_request"

ballerina_timestamp = ""
ballerina_lang_version = ""
latest_ballerina_stable_version = ''
send_reminder_chat = sys.argv[1]


def main():
    global send_reminder_chat
    global lag_reminder_modules
    update_lang_version()

    updated_readme = get_updated_readme()

    # Write to local README file
    f = open(README_FILE, 'w')
    f.write(updated_readme)
    f.close()

    try:
        update_readme, commit = utils.commit_file('ballerina-release',
                                                  README_FILE, updated_readme,
                                                  constants.DASHBOARD_UPDATE_BRANCH,
                                                  '[Automated] Update extension dependency dashboard')
    except GithubException as e:
        print('Error occurred while committing README.md', e)
        sys.exit(1)

    try:
        image = Image.open(constants.PIE_CHART_IMAGE, mode='r')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')

        if update_readme:
            utils.commit_image_file('ballerina-release', constants.PIE_CHART_IMAGE, img_byte_arr.getvalue(),
                                    constants.DASHBOARD_UPDATE_BRANCH, '[Automated] Update status pie chart')

    except GithubException as e:
        print('Error occurred while committing status pie chart', e)
        sys.exit(1)

    if update_readme:
        utils.open_pr_and_merge('ballerina-release',
                                '[Automated] Update Extension Dependency Dashboard',
                                'Update extension dependency dashboard',
                                constants.DASHBOARD_UPDATE_BRANCH)
        if send_reminder_chat == 'true' and len(lag_reminder_modules) > 0:
            chat_message = distribution_lag_statement.replace('<code>ballerina-distribution</code>',
                                                              '*ballerina-distribution*') + ".\n\n"
            chat_message += "*Reminder* on the following modules\' dependency update..." + "\n"
            for module in lag_reminder_modules:
                lag_status_link = module[MODULE_PULL_REQUEST]
                if lag_status_link == "":
                    lag_status_link = constants.BALLERINA_ORG_URL + module[MODULE_NAME]
                chat_message += utils.get_module_message(module, lag_status_link)
            print("\n" + utils.get_sanitised_chat_message(chat_message))
            notify_chat.send_message(chat_message)
    else:
        print('No changes to ' + README_FILE + ' file')


def get_lang_latest_timestamp():
    try:
        version_string = utils.get_latest_lang_version()
    except Exception as e:
        print('[Error] Failed to get ballerina packages version', e)
        sys.exit(1)
    lang_version = version_string.split("-")
    if len(lang_version) > 3:
        timestamp = create_timestamp(lang_version[1], lang_version[2])
    else:
        timestamp = 0

    return timestamp


def update_lang_version():
    global ballerina_lang_version
    global ballerina_timestamp
    global latest_ballerina_stable_version

    data = utils.read_json_file(constants.LANG_VERSION_FILE)
    ballerina_lang_version = data["version"]
    lang_version = ballerina_lang_version.split("-")

    if len(lang_version) > 3:
        ballerina_timestamp = create_timestamp(lang_version[1], lang_version[2])
    else:
        ballerina_timestamp = -3
    latest_ballerina_stable_version = '-'.join(ballerina_lang_version.split('-')[0:1])


def days_hours_minutes(td):
    return td.days, td.seconds // 3600


def create_timestamp(date, time):
    timestamp = datetime(int(date[0:4]),
                         int(date[4:6]),
                         int(date[6:8]),
                         int(time[0:2]),
                         int(time[2:4]),
                         int(time[4:6]))
    return timestamp


def format_lag(timestamp):
    global ballerina_timestamp
    if timestamp == -1 or timestamp == -2:
        return timestamp, 0
    if ballerina_timestamp == -3:
        return -2, 0
    days, hours = days_hours_minutes(abs(ballerina_timestamp - timestamp))
    if days > 0:
        hrs = round((hours / 24) * 2) / 2
        days = days + hrs
        if days.is_integer():
            days = int(days)

    return days, hours


def get_lag_color(lag_days, lag_hrs):
    if lag_days == 0 and lag_hrs == 0:
        color = "brightgreen"
    elif 0 <= lag_days < 2:
        color = "yellow"
    elif ballerina_timestamp == -3 and lag_days == -1:
        color = "brightgreen"
    else:
        color = "red"

    return color


def get_lag_info(module_name):
    global latest_ballerina_stable_version
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    properties_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE)
    properties_file = properties_file.decoded_content.decode(constants.ENCODING)

    for line in properties_file.splitlines():
        if line.startswith(constants.LANG_VERSION_KEY):
            current_version = line.split("=")[-1]
            split_timestamp_string = current_version.split("-")
            if current_version == latest_ballerina_stable_version:
                timestamp = -1
            elif '-'.join(split_timestamp_string[0:1]) == latest_ballerina_stable_version:
                timestamp = create_timestamp(split_timestamp_string[1], split_timestamp_string[2])
            else:
                if len(split_timestamp_string) > 2:
                    timestamp = -2
                else:
                    # This is in stable version
                    timestamp = -1

    days, hrs = format_lag(timestamp)

    color = get_lag_color(days, hrs)

    return days, hrs, color


def get_lag_button(module):
    global modules_with_no_lag
    lag = False
    #days, hrs, color = get_lag_info(module[MODULE_NAME])
    days, hrs, color = -1, 0, "brightgreen"
    if days > 1:
        lag_status = str(days) + "%20days"
        lag = True
    elif days > 0:
        lag_status = str(days) + "%20day"
        lag = True
    elif days == 0 and hrs > 0:
        lag_status = str(hrs) + "%20h"
        lag = True
    elif days == -1:
        if ballerina_timestamp == -3:
            lag_status = "no%20lag"
            modules_with_no_lag += 1
        else:
            lag_status = "Latest%20Stable%20Version"
            lag = True
    elif days == -2:
        lag_status = "Previous%20Development%20Version"
        lag = True
    else:
        lag_status = "no%20lag"
        modules_with_no_lag += 1

    lag_status_link = "https://github.com/ballerina-platform/" + module[MODULE_NAME] \
                      + "/blob/" + module["default_branch"] + "/" + constants.GRADLE_PROPERTIES_FILE
    lag_button = "[![Lag](https://img.shields.io/badge/lag-" + lag_status + "-" + color + "?label=)](" \
                 + lag_status_link + ")"

    return lag_button, lag


def get_pending_pr(module):
    pr_id = ""
    pending_pr_link = ""
    pr = get_pending_automated_pr(module[MODULE_NAME])

    if pr is not None:
        pr_id = "#" + str(pr.number)
        pending_pr_link = pr.html_url
    pending_pr_button = "[" + pr_id + "](" + pending_pr_link + ")"

    return pending_pr_button, pending_pr_link


def update_modules(updated_readme, module_details_list, is_extended_library):
    global lag_reminder_modules
    global lagging_modules_level

    module_details_list.sort(reverse=True, key=lambda s: s['level'])
    last_level = module_details_list[0]['level']

    for i in range(last_level):
        current_level = i + 1
        current_level_modules = list(filter(lambda s: s['level'] == current_level, module_details_list))

        for idx, module in enumerate(current_level_modules):
            if module[MODULE_NAME].startswith("module"):
                name = module[MODULE_NAME].split("-")[2]
                if module[MODULE_NAME].split("-")[1] == "ballerinai":
                    name = name + "i"
            else:
                name = module[MODULE_NAME]

            build_button = "[![Build](" + constants.BALLERINA_ORG_URL + module['name'] + \
                           "/actions/workflows/" + module[MODULE_BUILD_ACTION_FILE] + ".yml/badge.svg)]" + \
                           "(" + constants.BALLERINA_ORG_URL + module['name'] + "/actions/workflows/" + \
                           module[MODULE_BUILD_ACTION_FILE] + ".yml)"
            lag_button, lag = get_lag_button(module)
            pending_pr_button, pending_pr_link = get_pending_pr(module)

            if (not is_extended_library) and is_distribution_lagging and lag:
                module[MODULE_PULL_REQUEST] = pending_pr_link
                if lagging_modules_level == 0:
                    # All modules have been up to date so far
                    lag_reminder_modules.append(module)
                    lagging_modules_level = module['level']
                elif module['level'] == lagging_modules_level:
                    lag_reminder_modules.append(module)

            level = ""
            if idx == 0:
                level = str(current_level)

            table_row = "| " + level + " | [" + name + "](" + constants.BALLERINA_ORG_URL + module[
                MODULE_NAME] + ") | " + build_button + " | " + lag_button + " | " + pending_pr_button + " | "
            updated_readme += table_row + "\n"

    return updated_readme


def get_lang_version_statement():
    ballerina_timestamp = get_lang_latest_timestamp()
    days, hrs = format_lag(ballerina_timestamp)
    ballerina_lang_lag = ""

    if days == 1:
        ballerina_lang_lag = str(days) + " day"
    elif days > 1:
        ballerina_lang_lag = str(days) + " days"
    elif hrs > 0:
        ballerina_lang_lag = str(hrs) + " h"

    if not ballerina_lang_lag:
        lang_version_statement = "<code>ballerina-lang</code> repository version <b>" + ballerina_lang_version + \
                                 "</b> has been updated as follows"
    else:
        lang_version_statement = "<code>ballerina-lang</code> repository version <b>" + ballerina_lang_version + \
                                 "</b> (" + ballerina_lang_lag + ") has been updated as follows"

    return lang_version_statement


def get_distribution_statement():
    global is_distribution_lagging
    global distribution_lag_statement

    BALLERINA_DISTRIBUTION = "ballerina-distribution"
    days, hrs = get_lag_info(BALLERINA_DISTRIBUTION)[0:2]
    distribution_lag = ""

    distribution_pr = get_pending_automated_pr(BALLERINA_DISTRIBUTION)

    if days == -2:
        distribution_lag = "previous development version"
    if days == -1:
        distribution_lag = "latest stable version"
    elif days == 1:
        distribution_lag = str(days) + " day"
    elif days > 1:
        distribution_lag = str(days) + " days"
    elif hrs > 0:
        distribution_lag = str(hrs) + " h"

    if not distribution_lag:
        distribution_lag_statement = "<code>ballerina-distribution</code> repository is up to date."
    else:
        is_distribution_lagging = True
        if days < 0:
            distribution_lag_statement = "<code>ballerina-distribution</code> repository has not been updated from the " + distribution_lag
        else:
            distribution_lag_statement = "<code>ballerina-distribution</code> repository lags by " + distribution_lag

        if distribution_pr is None:
            distribution_lag_statement += "."
        else:
            distribution_lag_statement += " and pending PR " + "<a href='" + \
                                          distribution_pr.html_url + "'>#" + str(distribution_pr.number) + \
                                          "</a>  is available."

    return distribution_lag_statement


def get_updated_readme():
    updated_readme = ""
    global all_modules

    all_modules = utils.read_json_file(constants.EXTENSIONS_FILE)
    module_details_list = all_modules["standard_library"]

    # lang_version_statement = get_lang_version_statement()
    # distribution_statement = get_distribution_statement()
    lang_version_statement = "<code>ballerina-lang</code> repository version <b>2201.0.1-rc3.1</b> has been updated as follows"
    distribution_statement = "<code>ballerina-distribution</code> repository is up to date."

    updated_readme += "# Ballerina Repositories Update Status\n\n" + \
                      "<table><tbody><tr>\n" + \
                      "<td align='center'><img src='" + constants.PIE_CHART_IMAGE + "'/></td>\n" + \
                      "<td align='center'>\n"

    updated_readme += distribution_statement + "<br><br>\n"
    updated_readme += lang_version_statement + "\n</td>\n</tr></tbody></table> \n\n "

    updated_readme += "## Ballerina Standard Library" + "\n"
    updated_readme += "| Level | Modules | Build | Lag Status | Pending Automated PR |" + "\n"
    updated_readme += "|:---:|:---:|:---:|:---:|:---:|" + "\n"

    updated_readme = update_modules(updated_readme, module_details_list, False)

    updated_readme += "## Ballerina library" + "\n"

    updated_readme += "| Level | Modules | Build | Lag Status | Pending Automated PR |" + "\n"
    updated_readme += "|:---:|:---:|:---:|:---:|:---:|" + "\n"

    extended_library = all_modules["extended_library"]

    updated_readme = update_modules(updated_readme, extended_library, True)

    repositories_updated = round((modules_with_no_lag / (len(module_details_list) + len(extended_library))) * 100)
    make_pie(repositories_updated)

    return updated_readme


def make_pie(val):
    sizes = [val, 100 - val]
    text = str(val) + "%"

    if val == 100:
        edge_color = 'forestgreen'
    else:
        edge_color = 'ivory'

    fig, ax = plt.subplots()
    ax.axis('equal')
    kwargs = dict(colors=['forestgreen', 'firebrick'], startangle=180)
    outside, _ = ax.pie(sizes, radius=1, pctdistance=0.325, **kwargs)
    plt.setp(outside, width=0.35, edgecolor=edge_color)
    kwargs = dict(size=20, fontweight='bold', va='center')
    ax.text(0, 0, text, ha='center', **kwargs)
    plt.savefig(constants.PIE_CHART_IMAGE)


def get_pending_automated_pr(module_name):
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    pulls = repo.get_pulls(state="open")

    for pull in pulls:
        if pull.head.ref == constants.DEPENDENCY_UPDATE_BRANCH:
            return pull
    return None


main()
