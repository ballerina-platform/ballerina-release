from github import Github, InputGitAuthor, GithubException
import json
import os
from retry import retry
import sys
import time
import urllib.request
import json

HTTP_REQUEST_RETRIES = 3
HTTP_REQUEST_DELAY_IN_SECONDS = 2
HTTP_REQUEST_DELAY_MULTIPLIER = 2

ORGANIZATION = "ballerina-platform"
LANG_VERSION_KEY = "ballerinaLangVersion"
VERSION_KEY = "version="

LANG_VERSION_UPDATE_BRANCH = 'automated/dependency_version_update'
MASTER_BRANCH = "master"
MAIN_BRANCH = "main"

packageUser = os.environ["packageUser"]
packagePAT = os.environ["packagePAT"]
packageEmail = os.environ["packageEmail"]

ENCODING = "utf-8"

OPEN = "open"
MODULES = "modules"

COMMIT_MESSAGE_PREFIX = "[Automated] Update lang version to "
PULL_REQUEST_BODY_PREFIX = "Update ballerina lang version to `"
PULL_REQUEST_TITLE = "[Automated] Update Dependencies"

MODULE_LIST_FILE = "dependabot/resources/module_list.json"
PROPERTIES_FILE = "gradle.properties"

overrideBallerinaVersion = sys.argv[1]

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


def check_and_update_lang_version(module_list_json, lang_version):
    for module_name in module_list_json[MODULES]:
        update_module(module_name, lang_version)


def update_module(module_name, lang_version):
    github = Github(packagePAT)
    repo = github.get_repo(ORGANIZATION + "/" + module_name)
    try:
        properties_file = repo.get_contents(PROPERTIES_FILE, ref=LANG_VERSION_UPDATE_BRANCH)
    except:
        properties_file = repo.get_contents(PROPERTIES_FILE)

    properties_file = properties_file.decoded_content.decode(ENCODING)
    update, updated_properties_file = get_updated_properties_file(module_name, properties_file, lang_version)
    if update:
        commit_changes(repo, updated_properties_file, lang_version)
        create_pull_request(repo, lang_version)
        time.sleep(30)


def get_updated_properties_file(module_name, properties_file, lang_version):
    updated_properties_file = ""
    update = False

    splitLangVersion = lang_version.split('-')
    processedLangVersion = splitLangVersion[2] + splitLangVersion[3]

    for line in properties_file.splitlines():
        if line.startswith(LANG_VERSION_KEY):
            current_version = line.split("=")[-1]

            splitCurrentVersion = current_version.split('-')
            processedCurrentVersion = splitCurrentVersion[2] + splitCurrentVersion[3]

            if processedCurrentVersion < processedLangVersion:
                print("[Info] Updating the lang version in module: \"" + module_name + "\"")
                updated_properties_file += LANG_VERSION_KEY + "=" + lang_version + "\n"
                update = True
            else:
                updated_properties_file += line + "\n"
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


def create_pull_request(repo, lang_version):
    pulls = repo.get_pulls(state=OPEN, head=LANG_VERSION_UPDATE_BRANCH)
    pr_exists = False

    for pull in pulls:
        if PULL_REQUEST_TITLE in pull.title:
            pr_exists = True

    if not pr_exists:
        try:
            repo.create_pull(
                title=PULL_REQUEST_TITLE,
                body=PULL_REQUEST_BODY_PREFIX + lang_version + "`",
                head=LANG_VERSION_UPDATE_BRANCH,
                base=MASTER_BRANCH
            )
        except:
            repo.create_pull(
                title=PULL_REQUEST_TITLE,
                body=PULL_REQUEST_BODY_PREFIX + lang_version + "`",
                head=LANG_VERSION_UPDATE_BRANCH,
                base=MAIN_BRANCH
            )
main()
