import json
import requests
import constants
import os
import sys


stdlib_modules_by_level = dict()
stdlib_modules_json_file = 'https://raw.githubusercontent.com/ballerina-platform/ballerina-standard-library/' \
                               'main/release/resources/stdlib_modules.json'
stdlib_module_versions = dict()
ballerina_lang_branch = "master"
exit_code = 0

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]


def main():
    global stdlib_modules_by_level
    global stdlib_modules_json_file
    global stdlib_module_versions
    global ballerina_lang_branch

    if len(sys.argv) > 1:
        ballerina_lang_branch = sys.argv[1]

    read_stdlib_modules()
    if stdlib_modules_by_level:
        clone_repositories()
        change_version_to_snapshot()
        build_stdlib_repositories(ballerina_lang_branch)
    else:
        print('Could not find standard library dependency data from', stdlib_modules_json_file)


def read_stdlib_modules():
    try:
        response = requests.get(url=stdlib_modules_json_file)

        if response.status_code == 200:
            stdlib_modules_data = json.loads(response.text)
            read_dependency_data(stdlib_modules_data)
        else:
            print('Failed to access standard library dependency data from', stdlib_modules_json_file)
            sys.exit(1)

    except json.decoder.JSONDecodeError:
        print('Failed to load standard library dependency data')
        sys.exit(1)


def read_dependency_data(stdlib_modules_data):
    for module in stdlib_modules_data['modules']:
        parent = module['name']
        level = module['level']
        stdlib_modules_by_level[level] = stdlib_modules_by_level.get(level, []) + [parent]


def clone_repositories():
    global exit_code

    # Clone ballerina-lang repo
    exit_code = os.system(f"git clone {constants.BALLERINA_ORG_URL}ballerina-lang.git")
    if exit_code != 0:
        sys.exit(1)

    # Clone standard library repos
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            exit_code = os.system(f"git clone {constants.BALLERINA_ORG_URL}{module}.git")
            if exit_code != 0:
                sys.exit(1)


def build_stdlib_repositories(ballerina_lang_branch):
    global exit_code

    # Build ballerina-lang repo
    os.system(f"cd ballerina-lang;git checkout {ballerina_lang_branch}")
    os.system("cd ballerina-lang;git status")
    exit_code = os.system("cd ballerina-lang;./gradlew clean build -x test publishToMavenLocal")
    if exit_code != 0:
        print(f"Build failed for ballerina-lang")
        sys.exit(1)

    # Build standard library repos
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            os.system(f"echo Building Standard Library Module: {module}")
            exit_code = os.system(f"cd {module};" +
                                  f"export packageUser={ballerina_bot_username};" +
                                  f"export packagePAT={ballerina_bot_token};" +
                                  f"./gradlew clean build publishToMavenLocal")
            if exit_code != 0:
                print(f"Build failed for {module}")
                sys.exit(1)


def change_version_to_snapshot():
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            try:
                properties = dict()
                with open(f"{module}/gradle.properties", 'r') as config_file:
                    for line in config_file:
                        try:
                            name, value = line.split("=")
                            if "stdlib" in name:
                                version = value.split("-")[0]
                                value = version + "-SNAPSHOT\n"
                            elif "ballerinaLangVersion" in name:
                                version = value.split("-")[0] + "-" + value.split("-")[1]
                                value = version + "-SNAPSHOT\n"
                            properties[name] = value
                        except ValueError:
                            continue
                    config_file.close()

                with open(f"{module}/gradle.properties", 'w') as config_file:
                    for prop in properties:
                        config_file.write(prop + "=" + properties[prop])
                    config_file.close()

            except FileNotFoundError:
                print(f"Cannot find the gradle.properties file for {module}")
                sys.exit(1)
    print("Updated dependent standard library versions to SNAPSHOT")


main()
