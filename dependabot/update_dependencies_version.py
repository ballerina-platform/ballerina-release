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

github = Github(packagePAT)

def main():
    lang_version = get_lang_version()
    module_list_json = get_module_list_json()
    check_and_update_lang_version(module_list_json, lang_version)

def get_lang_version():
    if (overrideBallerinaVersion != ''):
        return overrideBallerinaVersion
    else:
        try:
            versionString = open_url(
                "https://api.github.com/orgs/ballerina-platform/packages/maven/org.ballerinalang.jballerina-tools/versions").read()
        except Exception as e:
            print('[Error] Failed to get ballerina packages version', e)
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
        print("[Error] Error while loading modules list ", e)
        sys.exit(1)

    return module_list


def check_and_update_lang_version(module_list_json, lang_version):

    module_details_list = module_list_json[MODULES]
    module_details_list.sort(reverse=True, key=lambda s: s['level'])
    last_level = module_details_list[0]['level']

    for i in range(last_level):
        current_level = i + 1
        current_level_modules = list(filter(lambda s: s['level'] == current_level, module_list_json[MODULES]))

        for module in current_level_modules:
            print ("[Info] Update lang dependency in module '" + module[MODULE_NAME] + "'")
            module[MODULE_CREATED_PR] = update_module(module, lang_version)
            module[MODULE_PR_CHECK_STATUS] = "pending"

        if (autoMergePRs.lower() == "true"):
            wait_for_current_level_pr_build(current_level_modules, current_level)

def wait_for_current_level_pr_build(modules_list, level):
    print("[Info] Waiting for level '" + str(level) + "' module pr checks.")
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
                check_pending_pr_checks(modules_list, idx, pr_passed_modules, pr_failed_modules)

        if (len(pr_passed_modules) + len(pr_failed_modules)) == len(modules_list):
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
                print("[Info] Automated version bump PR merged for module '" + module[MODULE_NAME] + "'. PR: " + pr.html_url)
            except:
                print ("[Error] Error occurred while merging dependency PR for module '" + module[MODULE_NAME] + "'", e)
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

def check_pending_pr_checks(modules_list, index, pr_passed_modules, pr_failed_modules):
    print("[Info] Checking the status of the dependency bump PR in module '" + modules_list[index][MODULE_NAME] + "'")
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

def update_module(module, lang_version):
    repo = github.get_repo(ORGANIZATION + "/" + module[MODULE_NAME])
    properties_file = repo.get_contents(PROPERTIES_FILE)

    properties_file = properties_file.decoded_content.decode(ENCODING)
    update, updated_properties_file = get_updated_properties_file(module[MODULE_NAME], properties_file, lang_version)
    if update:
        commit_changes(repo, updated_properties_file, lang_version, module[MODULE_NAME])
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
                    print("[Info] Updating the lang version in module: '" + module_name + "'")
                    updated_properties_file += LANG_VERSION_KEY + "=" + lang_version + "\n"
                    update = True
                else:
                    updated_properties_file += line + "\n"
            else:
                # Stable dependency & SNAPSHOT
                print("[Info] Updating the lang version in module: '" + module_name + "'")
                updated_properties_file += LANG_VERSION_KEY + "=" + lang_version + "\n"
                update = True
        else:
            updated_properties_file += line + "\n"

    return update, updated_properties_file


def commit_changes(repo, updated_file, lang_version, module_name):
    author = InputGitAuthor(packageUser, packageEmail)
    base = repo.get_branch(repo.default_branch)
    branch = LANG_VERSION_UPDATE_BRANCH

    try:
        ref = f"refs/heads/" + branch
        repo.create_git_ref(ref=ref, sha=base.commit.sha)
    except :
        print("[Info] Unmerged update branch existed in module: '" + module_name + "'")
        branch = LANG_VERSION_UPDATE_BRANCH + "_update_tmp"
        ref = f"refs/heads/" + branch
        try:
            repo.create_git_ref(ref=ref, sha=base.commit.sha)
        except GithubException as e:
            print("[Info] deleting update tmp branch existed in module: '" + module_name + "'")
            if e.status == 422: # already exist
                repo.get_git_ref("heads/" + branch).delete()
                repo.create_git_ref(ref=ref, sha=base.commit.sha)

    remote_file = repo.get_contents(PROPERTIES_FILE, ref=LANG_VERSION_UPDATE_BRANCH)
    remote_file_contents = remote_file.decoded_content.decode("utf-8")

    if (remote_file_contents == updated_file):
        print("[Info] Branch with the lang version is already present.")
    else:
        current_file = repo.get_contents(PROPERTIES_FILE, ref=branch)
        update = repo.update_file(
            current_file.path,
            COMMIT_MESSAGE_PREFIX + lang_version,
            updated_file,
            current_file.sha,
            branch=branch,
            author=author
        )
        if not branch == LANG_VERSION_UPDATE_BRANCH:
            update_branch = repo.get_git_ref("heads/" + LANG_VERSION_UPDATE_BRANCH)
            update_branch.edit(update["commit"].sha, force=True)
            repo.get_git_ref("heads/" + branch).delete()

def create_pull_request(module, repo, lang_version):
    pulls = repo.get_pulls(state=OPEN, head=LANG_VERSION_UPDATE_BRANCH)
    pr_exists = False
    created_pr = ""

    shaOfLang = lang_version.split("-")[-1]

    for pull in pulls:
        if pull.head.ref == LANG_VERSION_UPDATE_BRANCH:
            pr_exists = True
            created_pr = pull
            pull.edit(
                title = pull.title.rsplit("-", 1)[0] + "-" + shaOfLang + ")",
                body = pull.body.rsplit("-", 1)[0] + "-" + shaOfLang + "`"
                )
            print("[Info] Automated version bump PR found for module '" + module[MODULE_NAME] + "'. PR: " + pull.html_url)
            break

    if not pr_exists:
        try:
            pull_request_title = PULL_REQUEST_TITLE
            if ((autoMergePRs.lower() == "true") & module[MODULE_AUTO_MERGE]):
                pull_request_title = AUTO_MERGE_PULL_REQUEST_TITLE
            pull_request_title = pull_request_title + lang_version + ")"

            created_pr = repo.create_pull(
                title=pull_request_title,
                body=PULL_REQUEST_BODY_PREFIX + lang_version + "`",
                head=LANG_VERSION_UPDATE_BRANCH,
                base=repo.default_branch
            )
            print("[Info] Automated version bump PR created for module '" + module[MODULE_NAME] + "'. PR: " + created_pr.html_url)
        except Exception as e:
            print ("[Error] Error occurred while creating pull request for module '" + module[MODULE_NAME] + "'.", e)
            sys.exit(1)
        if ((autoMergePRs.lower() == "true") & module[MODULE_AUTO_MERGE]):

            # To stop intermittent failures due to API sync
            time.sleep(5)

            r_github = Github(reviewerPackagePAT)
            repo = r_github.get_repo(ORGANIZATION + "/" + module[MODULE_NAME])
            pr = repo.get_pull(created_pr.number)
            try:
                pr.create_review(event="APPROVE")
                print("[Info] Automated version bump PR approved for module '" + module[MODULE_NAME] + "'. PR: " + pr.html_url)
            except:
                print ("[Error] Error occurred while approving dependency PR for module '" + module[MODULE_NAME] + "'", e)
                sys.exit(1)

    return created_pr

main()
