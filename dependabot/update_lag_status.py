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

MODULE_NAME = "name"
MODULE_BUILD_ACTION_FILE = "build_action_file"
ballerina_timestamp = ""
ballerina_lang_version = ""


def main():
    update_lang_version()

    updated_readme = get_updated_readme()

    # Write to local README file
    f = open(README_FILE, 'w')
    f.write(updated_readme)
    f.close()

    try:
        update, commit = utils.commit_file('ballerina-release',
                                           README_FILE, updated_readme,
                                           constants.DASHBOARD_UPDATE_BRANCH,
                                           '[Automated] Update extension dependency dashboard')
    except GithubException as e:
        print('Error occurred while committing README.md', e)
        sys.exit(1)

    try:
        image = Image.open('dependabot/resources/repo_status_graph.jpeg', mode='r')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')

        update, _ = utils.commit_file('ballerina-release',
                                      constants.PIE_CHART_IMAGE, img_byte_arr.getvalue(),
                                      constants.DASHBOARD_UPDATE_BRANCH,
                                      '[Automated] Update status pie chart', False)
    except GithubException as e:
        print('Error occurred while committing status pie chart', e)
        sys.exit(1)

    if update:
        utils.open_pr_and_merge('ballerina-release',
                                '[Automated] Update Extension Dependency Dashboard',
                                'Update extension dependency dashboard',
                                constants.DASHBOARD_UPDATE_BRANCH)
        notify_chat.notify_lag_update(commit)
    else:
        print('No changes to ' + README_FILE + ' file')


def get_lang_version_lag():
    global ballerina_timestamp
    try:
        version_string = utils.get_latest_lang_version()
    except Exception as e:
        print('[Error] Failed to get ballerina packages version', e)
        sys.exit(1)
    lang_version = version_string.split("-")
    timestamp = create_timestamp(lang_version[2], lang_version[3])
    ballerina_lag = timestamp - ballerina_timestamp

    return ballerina_lag


def update_lang_version():
    global ballerina_lang_version
    global ballerina_timestamp

    data = utils.read_json_file(constants.LANG_VERSION_FILE)
    ballerina_lang_version = data["version"]
    lang_version = ballerina_lang_version.split("-")
    ballerina_timestamp = create_timestamp(lang_version[2], lang_version[3])


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


def format_lag(delta):
    days, hours = days_hours_minutes(delta)
    if days > 0:
        hrs = round((hours / 24) * 2) / 2
        days = days + hrs
        if days.is_integer():
            days = int(days)

    return days, hours


def get_lag_color(lag_days, lag_hrs):
    if lag_days == 0 and lag_hrs == 0:
        color = "brightgreen"
    elif lag_days < 2:
        color = "yellow"
    else:
        color = "red"

    return color


def get_lag_info(module_name):
    global ballerina_timestamp
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    properties_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE)
    properties_file = properties_file.decoded_content.decode(constants.ENCODING)

    for line in properties_file.splitlines():
        if line.startswith(constants.LANG_VERSION_KEY):
            current_version = line.split("=")[-1]
            timestamp_string = current_version.split("-")[2:4]
            timestamp = create_timestamp(timestamp_string[0], timestamp_string[1])

    update_timestamp = ballerina_timestamp - timestamp
    days, hrs = format_lag(update_timestamp)

    color = get_lag_color(days, hrs)

    return days, hrs, color


def get_lag_button(module):
    global modules_with_no_lag
    days, hrs, color = get_lag_info(module[MODULE_NAME])
    if days > 0:
        lag_status = str(days) + "%20days"
    elif hrs > 0:
        lag_status = str(hrs) + "%20h"
    else:
        lag_status = "no%20lag"
        modules_with_no_lag += 1

    lag_status_link = "https://github.com/ballerina-platform/" + module[MODULE_NAME] \
                      + "/blob/" + module["default_branch"] + "/" + constants.GRADLE_PROPERTIES_FILE
    lag_button = "[![Lag](https://img.shields.io/badge/lag-" + lag_status + "-" + color + "?label=)](" \
                 + lag_status_link + ")"

    return lag_button


def get_pending_pr(module):
    pr_id = ""
    pending_pr_link = ""
    pr_number = check_pending_pr_checks(module[MODULE_NAME])

    if pr_number is not None:
        pr_id = "#" + str(pr_number)
        pending_pr_link = "https://github.com/ballerina-platform/" + module[MODULE_NAME] + "/pull/" + str(
            pr_number)
    pending_pr = "[" + pr_id + "](" + pending_pr_link + ")"

    return pending_pr


def update_modules(updated_readme, module_details_list):
    module_details_list.sort(reverse=True, key=lambda s: s['level'])
    last_level = module_details_list[0]['level']

    for i in range(last_level):
        current_level = i + 1
        current_level_modules = list(filter(lambda s: s['level'] == current_level, module_details_list))

        for idx, module in enumerate(current_level_modules):
            if module[MODULE_NAME].startswith("module"):
                name = module[MODULE_NAME].split("-")[2]
            else:
                name = module[MODULE_NAME]

            build_button = "[![Build](" + constants.BALLERINA_ORG_URL + module['name'] + \
                           "/actions/workflows/" + module[MODULE_BUILD_ACTION_FILE] + ".yml/badge.svg)]" + \
                           "(" + constants.BALLERINA_ORG_URL + module['name'] + "/actions/workflows/" + \
                           module[MODULE_BUILD_ACTION_FILE] + ".yml)"
            lag_button = get_lag_button(module)
            pending_pr = get_pending_pr(module)

            level = ""
            if idx == 0:
                level = str(current_level)

            table_row = "| " + level + " | [" + name + "](" + constants.BALLERINA_ORG_URL + module[
                MODULE_NAME] + ") | " + build_button + " | " + lag_button + " | " + pending_pr + " | "
            updated_readme += table_row + "\n"
    return updated_readme


def get_lang_version_statement():
    ballerina_lag = get_lang_version_lag()
    days, hrs = format_lag(ballerina_lag)
    ballerina_lang_lag = ""

    if days > 0:
        ballerina_lang_lag = str(days) + " days"
    elif hrs > 0:
        ballerina_lang_lag = str(hrs) + " h"

    if not ballerina_lang_lag:
        lang_version_statement = "`ballerina-lang` repository version **" + ballerina_lang_version + \
                                 "** has been updated as follows"
    else:
        lang_version_statement = "`ballerina-lang` repository version **" + ballerina_lang_version + \
                                 "** (" + ballerina_lang_lag + ") has been updated as follows"

    return lang_version_statement


def get_distribution_statement():
    BALLERINA_DISTRIBUTION = "ballerina-distribution"
    days, hrs = get_lag_info(BALLERINA_DISTRIBUTION)[0:2]
    distribution_lag = ""

    distribution_pr_number = check_pending_pr_checks(BALLERINA_DISTRIBUTION)
    distribution_pr_link = "https://github.com/ballerina-platform/" + BALLERINA_DISTRIBUTION + "/pull/" + \
                           str(distribution_pr_number)

    if days > 0:
        distribution_lag = str(days) + " days"
    elif hrs > 0:
        distribution_lag = str(hrs) + " h"

    if not distribution_lag:
        distribution_lag_statement = "`ballerina-distribution` repository is up to date."
    else:
        if str(distribution_pr_number) == "None":
            distribution_lag_statement = "`ballerina-distribution` repository lags by " + distribution_lag
        else:
            distribution_lag_statement = "`ballerina-distribution` repository lags by " + distribution_lag + \
                                         " and pending PR [#" + str(distribution_pr_number) + "](" + \
                                         distribution_pr_link + ") is available"

    return distribution_lag_statement


def get_updated_readme():
    updated_readme = ""
    global all_modules

    all_modules = utils.read_json_file(constants.EXTENSIONS_FILE)
    module_details_list = all_modules["modules"]

    lang_version_statement = get_lang_version_statement()
    distribution_statement = get_distribution_statement()

    updated_readme += "# Ballerina Repositories Update Status\n\n" + \
                      "|![image alt](dependabot/resources/repo_status_graph.jpeg)|<div style='font-weight:normal'>"

    updated_readme += distribution_statement + "<br><br>"
    updated_readme += lang_version_statement + "</div>| \n |---|---| \n "

    updated_readme += "## Modules and Extensions Packed in Distribution" + "\n"
    updated_readme += "| Level | Modules | Build | Lag Status | Pending Automated PR |" + "\n"
    updated_readme += "|:---:|:---:|:---:|:---:|:---:|" + "\n"

    updated_readme = update_modules(updated_readme, module_details_list)

    updated_readme += "## Modules Released to Central" + "\n"

    updated_readme += "| Level | Modules | Build | Lag Status | Pending Automated PR |" + "\n"
    updated_readme += "|:---:|:---:|:---:|:---:|:---:|" + "\n"

    central_modules = all_modules["central_modules"]

    updated_readme = update_modules(updated_readme, central_modules)

    repositories_updated = round((modules_with_no_lag / (len(module_details_list) + len(central_modules))) * 100)
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
    kwargs = dict(colors=['forestgreen', 'red'], startangle=180)
    outside, _ = ax.pie(sizes, radius=1, pctdistance=0.325, **kwargs)
    plt.setp(outside, width=0.35, edgecolor=edge_color)
    kwargs = dict(size=20, fontweight='bold', va='center')
    ax.text(0, 0, text, ha='center', **kwargs)

    plt.savefig(constants.PIE_CHART_IMAGE)


def check_pending_pr_checks(module_name):
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    pulls = repo.get_pulls(state="open")

    for pull in pulls:
        if pull.head.ref == constants.DEPENDENCY_UPDATE_BRANCH:
            return pull.number
    return None


main()
