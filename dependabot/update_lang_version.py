from github import Github, InputGitAuthor, GithubException
import json
import os
from retry import retry
import sys
import time
import urllib.request

HTTP_REQUEST_RETRIES = 3
HTTP_REQUEST_DELAY_IN_SECONDS = 2
HTTP_REQUEST_DELAY_MULTIPLIER = 2

ORGANIZATION = "ballerina-platform"
LANG_VERSION_KEY = "ballerinaLangVersion"

LANG_VERSION_UPDATE_BRANCH = 'automated/dependency_version_update'
MASTER_BRANCH = "master"
MAIN_BRANCH = "main"

packageUser = os.environ["packageUser"]
packagePAT = os.environ["packagePAT"]
packageEmail = os.environ["packageEmail"]
reviewerPackagePAT = os.environ["reviewerPackagePAT"]

ENCODING = "utf-8"

OPEN = "open"
MODULES = "modules"

MODULE_NAME = "name"
MODULE_AUTO_MERGE = "auto_merge"
MODULE_CREATED_PR = "created_pr"
MODULE_PR_CHECK_STATUS = "pr_checks_status"
MODULE_FAILED_PR_CHECKS = "failed_pr_checks"

COMMIT_MESSAGE_PREFIX = "[Automated] Update lang version to "
PULL_REQUEST_BODY_PREFIX = "Update ballerina lang version to `"
PULL_REQUEST_TITLE = "[Automated] Update Dependencies (Ballerina Lang : "
AUTO_MERGE_PULL_REQUEST_TITLE = "[AUTO MERGE] Update Dependencies (Ballerina Lang : "

MODULE_LIST_FILE = "dependabot/resources/extensions.json"
PROPERTIES_FILE = "gradle.properties"

SLEEP_INTERVAL = 30 # 30s
MAX_WAIT_CYCLES = 80

overrideBallerinaVersion = sys.argv[1]
autoMergePRs = sys.argv[2]

def main():
    lang_version = get_lang_version()
    module_list_json = get_module_list_json()

    github = Github(packagePAT)
    check_and_update_lang_version(github, module_list_json, lang_version)

def get_lang_version():
    if (overrideBallerinaVersion != ''):
        return overrideBallerinaVersion
    else:
        try:
            versionString = open_url(
                "https://api.github.com/orgs/ballerina-platform/packages/maven/org.ballerinalang.jballerina-tools/versions").read()
        except Exception as e:
            print('Failed to get ballerina packages version', e)
            sys.exit(1)
        latestVersion = json.loads(versionString)[0]
        return latestVersion["name"]

@retry(
    urllib.error.URLError,
    tries=HTTP_REQUEST_RETRIES,
    delay=HTTP_REQUEST_DELAY_IN_SECONDS,
    backoff=HTTP_REQUEST_DELAY_MULTIPLIER
)
def open_url(url):
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github.v3+json")
    request.add_header("Authorization", "Bearer " + packagePAT)

    return urllib.request.urlopen(request)


def get_module_list_json():
    try:
        with open(MODULE_LIST_FILE) as f:
            module_list = json.load(f)

    except Exception as e:
        print(e)
        sys.exit(1)

    return module_list


def check_and_update_lang_version(github, module_list_json, lang_version):
    for module in module_list_json[MODULES]:
        print ("Update lang dependency in module '" + module[MODULE_NAME] + "'")
        module[MODULE_CREATED_PR] = update_module(github, module, lang_version)
        module[MODULE_PR_CHECK_STATUS] = "pending"

    if (autoMergePRs.lower() == "true"):
        module_details_list = module_list_json[MODULES]
        module_details_list.sort(reverse=True, key=lambda s: s['level'])
        last_level = module_details_list[0]['level']

        for i in range(last_level):
            current_level = i + 1
            current_level_modules = list(filter(lambda s: s['level'] == current_level, module_list_json[MODULES]))
            wait_for_current_level_pr_build(github, current_level_modules, current_level )

def wait_for_current_level_pr_build(github, modules_list, level):
    print("Waiting for level " + str(level) + " module pr checks.")
    totalModules = len(modules_list)

    time.sleep(SLEEP_INTERVAL)

    pr_passed_modules = []
    pr_failed_modules = []
    wait_cycles = 0
    all_modules_checked = False

    while (not all_modules_checked):
        for idx in range(len(modules_list)):
            module = modules_list[idx]
            if (module[MODULE_PR_CHECK_STATUS] == "pending"):
                check_pending_pr_checks(github, modules_list, idx, pr_passed_modules, pr_failed_modules)

        if len(modules_list) == 0:
            all_modules_checked = True
        elif wait_cycles < MAX_WAIT_CYCLES:
            time.sleep(SLEEP_INTERVAL)
            wait_cycles = wait_cycles + 1
        else:
            modules_list[idx][MODULE_PR_CHECK_STATUS] = "timed out"
            break

    all_prs_merged = True
    for module in pr_passed_modules:
        repo = github.get_repo(ORGANIZATION + "/" + module[MODULE_NAME])
        pr = repo.get_pull(module[MODULE_CREATED_PR].number)
        if (module[MODULE_AUTO_MERGE] & ("AUTO MERGE" in pr.title)):
            try:
                pr.merge()
            except:
                print ("Error occurred while merging dependency PR for module '" + module[MODULE_NAME] + "'", e)
                all_prs_merged = False

    if (len(pr_passed_modules) != totalModules):
        if len(pr_failed_modules) > 0:
            print ("Following modules dependency PRs have failed checks...")
            for module in pr_failed_modules:
                print (module[MODULE_NAME])
                for check in module[MODULE_FAILED_PR_CHECKS]:
                    print("[" + module[MODULE_NAME] + "] PR check '" + check["name"] + "' failed for " + check["html_url"])
        if len(modules_list) > 0:
            print ("Following modules dependency PRs check validation has timed out...")
            for module in modules_list:
                print (module[MODULE_NAME])
        sys.exit(1)

    if (not all_prs_merged):
        sys.exit(1)

def check_pending_pr_checks(github, modules_list, index, pr_passed_modules, pr_failed_modules):
    print("[" + modules_list[index][MODULE_NAME] + "] Checking status of the PR...")
    passing = True
    pending = False
    repo = github.get_repo(ORGANIZATION + "/" + modules_list[index][MODULE_NAME])
    sha = repo.get_pull(modules_list[index][MODULE_CREATED_PR].number).head.sha

    failed_pr_checks = []
    for pr_check in repo.get_commit(sha=sha).get_check_runs():
        if pr_check.conclusion == "success":
            continue
        elif pr_check.conclusion == "failure":
            failed_pr_check = {
                "name": pr_check.name,
                "html_url": pr_check.html_url
            }
            failed_pr_checks.append(failed_pr_check)
            passing = False
        else:
            pending = True
            break

    if (not pending):
        if passing:
            modules_list[index][MODULE_PR_CHECK_STATUS] = "success"
            pr_passed_modules.append(modules_list[index])
        else:
            modules_list[index][MODULE_PR_CHECK_STATUS] = "failure"
            modules_list[index][MODULE_FAILED_PR_CHECKS] = failed_pr_checks
            pr_failed_modules.append(modules_list[index])
        del(modules_list[index])

def update_module(github, module, lang_version):
    repo = github.get_repo(ORGANIZATION + "/" + module[MODULE_NAME])
    try:
        properties_file = repo.get_contents(PROPERTIES_FILE, ref=LANG_VERSION_UPDATE_BRANCH)
    except:
        properties_file = repo.get_contents(PROPERTIES_FILE)

    properties_file = properties_file.decoded_content.decode(ENCODING)
    update, updated_properties_file = get_updated_properties_file(module[MODULE_NAME], properties_file, lang_version)
    if update:
        commit_changes(repo, updated_properties_file, lang_version)
        return create_pull_request(module, repo, lang_version)


def get_updated_properties_file(module_name, properties_file, lang_version):
    updated_properties_file = ""
    update = False

    splitLangVersion = lang_version.split('-')
    processedLangVersion = splitLangVersion[2] + splitLangVersion[3]

    for line in properties_file.splitlines():
        if line.startswith(LANG_VERSION_KEY):
            current_version = line.split("=")[-1]

            splitCurrentVersion = current_version.split('-')

            if len(splitCurrentVersion) > 3:
                processedCurrentVersion = splitCurrentVersion[2] + splitCurrentVersion[3]

                if processedCurrentVersion < processedLangVersion:
                    print("[Info] Updating the lang version in module: \"" + module_name + "\"")
                    updated_properties_file += LANG_VERSION_KEY + "=" + lang_version + "\n"
                    update = True
                else:
                    updated_properties_file += line + "\n"
            else:
                # Stable dependency & SNAPSHOT
                print("[Info] Updating the lang version in module: \"" + module_name + "\"")
                updated_properties_file += LANG_VERSION_KEY + "=" + lang_version + "\n"
                update = True
        else:
            updated_properties_file += line + "\n"

    return update, updated_properties_file


def commit_changes(repo, updated_file, lang_version):
    author = InputGitAuthor(packageUser, packageEmail)
    try:
        base = repo.get_branch(MASTER_BRANCH)
    except:
        base = repo.get_branch(MAIN_BRANCH)

    try:
        ref = f"refs/heads/" + LANG_VERSION_UPDATE_BRANCH
        repo.create_git_ref(ref=ref, sha=base.commit.sha)
    except :
        try:
            repo.get_branch(LANG_VERSION_UPDATE_BRANCH)
            repo.merge(LANG_VERSION_UPDATE_BRANCH, base.commit.sha, "Sync default branch")
        except GithubException as e:
            print("Error occurred: ", e)


    current_file = repo.get_contents(PROPERTIES_FILE, ref=LANG_VERSION_UPDATE_BRANCH)
    repo.update_file(
        current_file.path,
        COMMIT_MESSAGE_PREFIX + lang_version,
        updated_file,
        current_file.sha,
        branch=LANG_VERSION_UPDATE_BRANCH,
        author=author
    )


def create_pull_request(module, repo, lang_version):
    pulls = repo.get_pulls(state=OPEN, head=LANG_VERSION_UPDATE_BRANCH)
    pr_exists = False
    created_pr = ""

    shaOfLang = lang_version[-7:]

    for pull in pulls:
        if (PULL_REQUEST_TITLE in pull.title) or (AUTO_MERGE_PULL_REQUEST_TITLE in pull.title) :
            pr_exists = True
            created_pr = pull
            newTitle = pull.title[0:-9]
            pull.edit(title = newTitle + shaOfLang + " )")

    if not pr_exists:
        try:
            pull_request_title = PULL_REQUEST_TITLE
            if module[MODULE_AUTO_MERGE]:
                pull_request_title = AUTO_MERGE_PULL_REQUEST_TITLE
            pull_request_title = pull_request_title + shaOfLang + " )"

            created_pr = repo.create_pull(
                title=pull_request_title,
                body=PULL_REQUEST_BODY_PREFIX + lang_version + "`",
                head=LANG_VERSION_UPDATE_BRANCH,
                base=MASTER_BRANCH
            )
        except Exception as e:
            print ("Error occurred while creating pull request for module '" + module_name + "'.", e)
            system.exit(1)
        if module[MODULE_AUTO_MERGE]:
            r_github = Github(reviewerPackagePAT)
            repo = r_github.get_repo(ORGANIZATION + "/" + module[MODULE_NAME])
            pr = repo.get_pull(created_pr.number)
            try:
                pr.create_review(event="APPROVE")
            except:
                print ("Error occurred while approving dependency PR for module '" + module_name + "'", e)
                system.exit(1)

    return created_pr

main()
