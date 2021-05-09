import json
import os
import sys
from datetime import datetime

from github import Github, GithubException

import constants
import utils

ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]

README_FILE = "README.md"
LANG_VERSION_KEY = "ballerinaLangVersion"

github = Github(ballerina_bot_token)

all_modules = []

MODULE_NAME = "name"
ballerina_timestamp = ""
ballerina_lang_version = ""


def main():

    update_lang_version()

    updated_readme = get_updated_readme()

    try:
        update = utils.commit_file('ballerina-release',
                                   README_FILE, updated_readme,
                                   constants.DASHBOARD_UPDATE_BRANCH,
                                   '[Automated] Update extension dependency dashboard')
        if update:
            utils.open_pr_and_merge('ballerina-release',
                                    '[Automated] Update Extension Dependency Dashboard',
                                    'Update extension dependency dashboard',
                                    constants.DASHBOARD_UPDATE_BRANCH)
    except GithubException as e:
        print('Error occurred while committing README.md', e)
        sys.exit(1)


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
    days, hrs = days_hours_minutes(ballerina_lag)
    if days > 0:
        lag_string = str(format_lag(ballerina_lag)) + " days"
    else:
        lag_string = str(hrs) + " h"

    return lag_string


def update_lang_version():
    global ballerina_lang_version
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/ballerina-release")
    lang_version_file = repo.get_contents(constants.LANG_VERSION_FILE)
    lang_version_json = lang_version_file.decoded_content.decode(constants.ENCODING)

    data = json.loads(lang_version_json)
    ballerina_lang_version = data["version"]


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
    hrs = round((hours / 24) * 2) / 2
    days = days + hrs
    if days.is_integer():
        days = int(days)
    return days


def get_lag_info(module_name):
    global ballerina_timestamp
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    properties_file = repo.get_contents(constants.GRADLE_PROPERTIES_FILE)
    properties_file = properties_file.decoded_content.decode(constants.ENCODING)

    for line in properties_file.splitlines():
        if line.startswith(LANG_VERSION_KEY):
            current_version = line.split("=")[-1]
            timestamp_string = current_version.split("-")[2:4]
            timestamp = create_timestamp(timestamp_string[0], timestamp_string[1])

    lang_version = ballerina_lang_version.split("-")
    ballerina_timestamp = create_timestamp(lang_version[2], lang_version[3])
    update_timestamp = ballerina_timestamp - timestamp
    delta = format_lag(update_timestamp)
    days = str(delta)

    if delta == 0:
        color = "brightgreen"
    elif delta < 2:
        color = "yellow"
    else:
        color = "red"

    return days, color


def update_modules(updated_readme, module_details_list):
    module_details_list.sort(reverse=True, key=lambda s: s['level'])
    last_level = module_details_list[0]['level']
    updated_modules = 0

    for i in range(last_level):
        current_level = i + 1
        current_level_modules = list(filter(lambda s: s['level'] == current_level, module_details_list))

        for idx, module in enumerate(current_level_modules):
            pr_id = ""

            pending_pr_link = ""

            if module[MODULE_NAME].startswith("module"):
                name = module[MODULE_NAME].split("-")[2]
            else:
                name = module[MODULE_NAME]

            lag_status, color = get_lag_info(module[MODULE_NAME])
            lag_status += "%20days"
            if color != "red":
                updated_modules += 1
            lag_button = "[![Lag](https://img.shields.io/badge/lag-" + lag_status + "-" + color + ")](#)"
            pr_number = check_pending_pr_checks(module[MODULE_NAME])

            if pr_number is not None:
                pr_id = "#" + str(pr_number)
                pending_pr_link = "https://github.com/ballerina-platform/" + module[MODULE_NAME] + "/pull/" + str(
                    pr_number)
            pending_pr = "[" + pr_id + "](" + pending_pr_link + ")"

            level = ""
            if idx == 0:
                level = str(current_level)

            table_row = "| " + level + " | [" + name + "](https://github.com/ballerina-platform/" + module[
                MODULE_NAME] + ") | " + lag_button + " | " + pending_pr + " | "
            updated_readme += table_row + "\n"
    return updated_readme, updated_modules


def get_updated_readme():
    BALLERINA_DISTRIBUTION = "ballerina-distribution"
    updated_readme = ""
    global all_modules

    all_modules = get_module_list()

    module_details_list = all_modules["modules"]
    distribution_lag = get_lag_info(BALLERINA_DISTRIBUTION)[0] + " days"

    ballerina_lang_lag = get_lang_version_lag()

    updated_readme += "# Ballerina Repositories Update Status" + "\n"
    distribution_pr_number = check_pending_pr_checks(BALLERINA_DISTRIBUTION)
    distribution_pr_link = "https://github.com/ballerina-platform/" + BALLERINA_DISTRIBUTION + "/pull/" + str(
        distribution_pr_number)

    if distribution_lag.startswith("0"):
        distribution_lag_statement = "`ballerina-distribution` repository is up to date."
    else:
        if str(distribution_pr_number) == "None":
            distribution_lag_statement = "`ballerina-distribution` repository lags by " + distribution_lag
        else:
            distribution_lag_statement = "`ballerina-distribution` repository lags by " + distribution_lag + " and pending PR [#" + str(
                distribution_pr_number) + "](" + distribution_pr_link + ") is available"

    if ballerina_lang_lag.startswith("0"):
        lang_version_statement = "`ballerina-lang` repository version **" + ballerina_lang_version + "** has been updated as follows"
    else:
        lang_version_statement = "`ballerina-lang` repository version **" + ballerina_lang_version + "** (" + ballerina_lang_lag + ") has been updated as follows"

    updated_readme += distribution_lag_statement + "<br>"
    updated_readme += "\n" + "<br>"
    updated_readme += lang_version_statement + "\n"

    updated_readme += "## Modules and Extensions Packed in Distribution" + "\n"
    updated_readme += "| Level | Modules | Lag Status | Pending PR |" + "\n"
    updated_readme += "|:---:|:---:|:---:|:---:|" + "\n"

    updated_readme, updated_modules_number = update_modules(updated_readme, module_details_list)

    updated_readme += "## Modules Released to Central" + "\n"

    updated_readme += "| Level | Modules | Lag Status | Pending PR |" + "\n"
    updated_readme += "|:---:|:---:|:---:|:---:|" + "\n"

    central_modules = all_modules["central_modules"]

    updated_readme, updated_modules_number_central = update_modules(updated_readme, central_modules)
    updated_modules_number += updated_modules_number_central
    repositories_updated = round((updated_modules_number / (len(module_details_list) + len(central_modules))) * 100)

    return updated_readme


def get_module_list():
    readme_repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/ballerina-release")

    module_list_json = readme_repo.get_contents(constants.EXTENSIONS_FILE)
    module_list_json = module_list_json.decoded_content.decode(constants.ENCODING)

    data = json.loads(module_list_json)

    return data


def check_pending_pr_checks(module_name):

    repo = github.get_repo(constants.BALLERINA_ORG_NAME + "/" + module_name)
    pulls = repo.get_pulls(state="open")

    for pull in pulls:
        if pull.head.ref == constants.DEPENDENCY_UPDATE_BRANCH:
            sha = pull.head.sha
            status = repo.get_commit(sha=sha).get_statuses()
            print(status)
            return pull.number
    return None


main()
