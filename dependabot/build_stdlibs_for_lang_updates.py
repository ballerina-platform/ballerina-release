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
enable_tests = 'true'
github_user = 'ballerina-platform'
exit_code = 0

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]


def main():
    global stdlib_modules_by_level
    global stdlib_modules_json_file
    global stdlib_module_versions
    global ballerina_lang_branch
    global github_user
    global enable_tests

    if len(sys.argv) > 2:
        ballerina_lang_branch = sys.argv[1]
        enable_tests = sys.argv[2]
        github_user = sys.argv[3]

    read_stdlib_modules()
    if stdlib_modules_by_level:
        clone_repositories()
        change_version_to_snapshot()
        build_stdlib_repositories(enable_tests)
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
        version = module['version']
        version_key = module['version_key']
        stdlib_modules_by_level[level] = stdlib_modules_by_level.get(level, []) + [parent]
        stdlib_module_versions[version_key] = version


def clone_repositories():
    global exit_code

    # Clone ballerina-lang repo
    exit_code = os.system(f"git clone https://github.com/{github_user}/ballerina-lang.git || " +
                          "echo 'please fork ballerina-lang repository to your github account'")
    if exit_code != 0:
        sys.exit(1)

    # Change branch
    os.system(f"cd ballerina-lang;git checkout {ballerina_lang_branch}")
    os.system("cd ballerina-lang;git status")

    # Clone standard library repos
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            exit_code = os.system(f"git clone {constants.BALLERINA_ORG_URL}{module}.git")
            if exit_code != 0:
                sys.exit(1)

    # Clone ballerina-distribution repo
    exit_code = os.system(f"git clone {constants.BALLERINA_ORG_URL}ballerina-distribution.git")
    if exit_code != 0:
        sys.exit(1)


def build_stdlib_repositories(enable_tests):
    global exit_code

    cmd_exclude_tests = ''
    if enable_tests == 'false':
        cmd_exclude_tests = ' -x test'
        print("Tests are disabled")
    else:
        print("Tests are enabled")

    # Build ballerina-lang repo
    exit_code = os.system(f"cd ballerina-lang;" +
                          f"./gradlew clean build -x test publishToMavenLocal --stacktrace --scan")
    if exit_code != 0:
        print(f"Build failed for ballerina-lang")
        write_failed_module("ballerina-lang")
        sys.exit(1)

    # Build standard library repos
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            os.system(f"echo Building Standard Library Module: {module}")
            exit_code = os.system(f"cd {module};" +
                                  f"export packageUser={ballerina_bot_username};" +
                                  f"export packagePAT={ballerina_bot_token};" +
                                  f"./gradlew clean build{cmd_exclude_tests} publishToMavenLocal --stacktrace --scan")
            if exit_code != 0:
                write_failed_module(module)
                print(f"Build failed for {module}")
                sys.exit(1)

    # Build ballerina-distribution repo
    os.system("echo Building ballerina-distribution")
    exit_code = os.system(f"cd ballerina-distribution;" +
                    f"export packageUser={ballerina_bot_username};" +
                    f"export packagePAT={ballerina_bot_token};" +
                    f"./gradlew clean build -x test " +
                    f"publishToMavenLocal --stacktrace --scan --console=plain --no-daemon --continue")
    if exit_code != 0:
        write_failed_module("ballerina-distribution")
        print(f"Build failed for ballerina-distribution")
        sys.exit(1)


def change_version_to_snapshot():
    # Read ballerina-lang version
    lang_version = ""
    with open("ballerina-lang/gradle.properties", 'r') as config_file:
        for line in config_file:
            try:
                name, value = line.split("=")
                if name == "version":
                    lang_version = value
            except ValueError:
                continue
        config_file.close()

    print("Lang Version:", lang_version)

    # Change dependent stdlib_module_versions & ballerina-lang version to SNAPSHOT in the stdlib modules
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            try:
                properties = dict()
                with open(f"{module}/gradle.properties", 'r') as config_file:
                    for line in config_file:
                        try:
                            name, value = line.split("=")
                            if name.startswith("stdlib"):
                                value = stdlib_module_versions[name] + "\n"
                            elif "ballerinaLangVersion" in name:
                                value = lang_version
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

    # Change dependent stdlib_module_versions & ballerina-lang version to SNAPSHOT in the ballerina-distribution
    properties = dict()
    with open("ballerina-distribution/gradle.properties", 'r') as config_file:
        for line in config_file:
            try:
                name, value = line.split("=")
                if name.startswith("stdlib"):
                    version = value.split("-")[0]
                    value = version + "-SNAPSHOT\n"
                elif "ballerinaLangVersion" in name:
                    value = lang_version
                properties[name] = value
            except ValueError:
                continue
        config_file.close()

    with open("ballerina-distribution/gradle.properties", 'w') as config_file:
        for prop in properties:
            config_file.write(prop + "=" + properties[prop])
        config_file.close()


def write_failed_module(module_name):
    with open("failed_module.txt", "w") as file:
        file.writelines(module_name)
        file.close()


main()
