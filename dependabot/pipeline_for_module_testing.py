import json
import requests
import constants
import os
import sys
from pathlib import Path


stdlib_modules_by_level = dict()
downstream_repo_branches = dict()
stdlib_modules_json_file = 'https://raw.githubusercontent.com/ballerina-platform/ballerina-release/master/' + \
                           'dependabot/resources/extensions.json'
test_ignore_modules_file = 'dependabot/resources/full_build_ignore_modules.json'

ballerina_lang_branch = "master"
downstream_repo_branch = "master"
enable_tests = 'true'
github_user = 'ballerina-platform'
test_module_name = ""
exit_code = 0

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]


def main():
    global stdlib_modules_by_level
    global stdlib_modules_json_file
    global test_ignore_modules_file
    global downstream_repo_branches
    global ballerina_lang_branch
    global downstream_repo_branch
    global test_module_name
    global github_user
    global enable_tests

    if len(sys.argv) > 2:
        ballerina_lang_branch = sys.argv[1]
        enable_tests = sys.argv[2]
        github_user = sys.argv[3]
        downstream_repo_branch = sys.argv[4]
        test_module_name = sys.argv[5]

    if test_module_name != "":
        read_stdlib_modules(test_module_name)
    else:
        print('Please specify the repository (module) name you need to test')

    if stdlib_modules_by_level:
        clone_repositories()
        change_version_to_snapshot()
        build_stdlib_repositories(enable_tests)
    else:
        print('Could not find standard library dependency data from', stdlib_modules_json_file)


def read_stdlib_modules(test_module_name):
    try:
        response = requests.get(url=stdlib_modules_json_file)

        if response.status_code == 200:
            stdlib_modules_data = json.loads(response.text)
            read_dependency_data(stdlib_modules_data, test_module_name)
        else:
            print('Failed to access standard library dependency data from', stdlib_modules_json_file)
            sys.exit(1)

    except json.decoder.JSONDecodeError:
        print('Failed to load standard library dependency data')
        sys.exit(1)


def read_dependency_data(stdlib_modules_data, test_module_name):
    standard_library_data = dict()
    module_dependencies = dict()
    for module in stdlib_modules_data['standard_library']:
        module_name = module['name']
        standard_library_data[module_name] = module
        dependents = module['dependents']
        for dependent in dependents:
            module_dependencies[dependent] = module_dependencies.get(dependent, []) + [module_name]

    module_list = {test_module_name}
    while module_list:
        current_module_name = module_list.pop()
        if current_module_name != test_module_name:
            level = standard_library_data[current_module_name]['level']
            version_key = standard_library_data[current_module_name]['version_key']
            if level in stdlib_modules_by_level.keys():
                repeated = False
                for module in stdlib_modules_by_level[level]:
                    if module["name"] == current_module_name:
                        repeated = True
                        break
                if not repeated:
                    stdlib_modules_by_level[level] = stdlib_modules_by_level.get(level, []) + \
                                                     [{"name": current_module_name, "version_key": version_key}]
            else:
                stdlib_modules_by_level[level] = [{"name": current_module_name, "version_key": version_key}]

        if current_module_name in module_dependencies.keys():
            dependencies = set(module_dependencies[current_module_name])
            module_list = module_list.union(dependencies)

    stdlib_levels = list(stdlib_modules_by_level.keys())
    stdlib_levels.sort()
    print("--------------------Following modules will be built with the pipeline--------------------")
    for level in stdlib_levels:
        print("Build Level:", level)
        module_names = [module['name'] for module in stdlib_modules_by_level[level]]
        print("Modules:", ", ".join(module_names))
    print("Testing Module:", test_module_name)


def clone_repositories():
    global exit_code

    # Clone ballerina-lang repo
    exit_code = os.system(f"git clone https://github.com/{github_user}/ballerina-lang.git || " +
                          "echo 'please fork ballerina-lang repository to your github account'")
    if exit_code != 0:
        sys.exit(1)

    # Change ballerina-lang branch
    exit_code = os.system(f"cd ballerina-lang;git checkout {ballerina_lang_branch}")
    os.system("cd ballerina-lang;git status")
    if exit_code != 0:
        sys.exit(1)

    # Clone standard library repos
    stdlib_levels = list(stdlib_modules_by_level.keys())
    stdlib_levels.sort()
    for level in stdlib_levels:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            module_name = module['name']
            exit_code = os.system(f"git clone {constants.BALLERINA_ORG_URL}{module_name}.git")
            if exit_code != 0:
                sys.exit(1)

            if downstream_repo_branch != "master":
                os.system(f"cd {module_name};git checkout {downstream_repo_branch}")
                os.system(f"cd {module_name};git status")
            else:
                if module_name in downstream_repo_branches.keys():
                    os.system(f"cd {module_name};git checkout {downstream_repo_branches[module_name]}")
                    os.system(f"cd {module_name};git status")

    # Clone module repository which needs to be tested
    exit_code = os.system(f"git clone {constants.BALLERINA_ORG_URL}{test_module_name}.git")
    if downstream_repo_branch != "master":
        os.system(f"cd {test_module_name};git checkout {downstream_repo_branch}")


def build_stdlib_repositories(enable_tests):
    global exit_code
    level_failed = False
    failed_modules = []

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
        failed_modules.append("ballerina-lang")
        write_failed_modules(failed_modules)
        sys.exit(1)
    delete_module('ballerina-lang')

    # Build standard library repos
    stdlib_levels = list(stdlib_modules_by_level.keys())
    stdlib_levels.sort()
    for level in stdlib_levels:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            os.system(f"echo Building Standard Library Module: {module['name']}")

            remove_dependency_files(module['name'])

            exit_code = os.system(f"cd {module['name']};" +
                                  f"export packageUser={ballerina_bot_username};" +
                                  f"export packagePAT={ballerina_bot_token};" +
                                  f"./gradlew clean build -x test publishToMavenLocal --stacktrace " +
                                  "--scan --console=plain --no-daemon --continue")

            if exit_code != 0:
                level_failed = True
                failed_modules.append(module['name'])
            delete_module(module['name'])

        if level_failed:
            write_failed_modules(failed_modules)
            sys.exit(1)

    # Build module which needs to be tested
    os.system(f"echo Building Testing Module: {test_module_name}")
    exit_code = os.system(f"cd {test_module_name};" +
                          f"export packageUser={ballerina_bot_username};" +
                          f"export packagePAT={ballerina_bot_token};" +
                          f"./gradlew clean build{cmd_exclude_tests} publishToMavenLocal --stacktrace " +
                          "--scan --console=plain --no-daemon --continue")
    if exit_code != 0:
        failed_modules.append(test_module_name)
        sys.exit(1)


def change_version_to_snapshot():
    # Read ballerina-lang version
    lang_version = ""
    with open("ballerina-lang/gradle.properties", 'r') as config_file:
        for line in config_file:
            try:
                name, value = line.split("=")
                if name == "version":
                    lang_version = value[:-1]
            except ValueError:
                continue
        config_file.close()

    print("Lang Version:", lang_version)

    # Read standard library module versions
    stdlib_module_versions = dict()
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            try:
                with open(f"{module['name']}/gradle.properties", 'r') as config_file:
                    for line in config_file:
                        try:
                            name, value = line.split("=")
                            if name == "version":
                                stdlib_module_versions[module['version_key']] = value[:-1]
                                break
                        except ValueError:
                            continue
                    config_file.close()
            except FileNotFoundError:
                print(f"Cannot find the gradle.properties file for {module}")
                sys.exit(1)

    # Print module versions
    for module_key in stdlib_module_versions:
        print(module_key + " : " + stdlib_module_versions[module_key])

    # Change dependent stdlib module versions & ballerina-lang version to SNAPSHOT in the stdlib modules
    for level in stdlib_modules_by_level:
        stdlib_modules = stdlib_modules_by_level[level]
        for module in stdlib_modules:
            try:
                properties = dict()
                with open(f"{module['name']}/gradle.properties", 'r') as config_file:
                    for line in config_file:
                        try:
                            fields = line.split("=")
                            if len(fields) > 1:
                                name = fields[0]
                                value = "=".join(fields[1:])
                                if name in stdlib_module_versions.keys():
                                    value = stdlib_module_versions[name] + "\n"
                                elif "ballerinaLangVersion" in name:
                                    value = lang_version + "\n"
                                properties[name] = value
                        except ValueError:
                            continue
                    if module['name'] == "module-ballerina-http":
                        properties["org.gradle.jvmargs"] = "-Xmx4096m -XX:MaxPermSize=512m"
                    config_file.close()

                with open(f"{module['name']}/gradle.properties", 'w') as config_file:
                    for prop in properties:
                        config_file.write(prop + "=" + properties[prop])
                    config_file.close()

            except FileNotFoundError:
                print(f"Cannot find the gradle.properties file for {module}")
                sys.exit(1)

    # Change dependent stdlib module versions & ballerina-lang version in module which needs to be tested
    properties = dict()
    with open(f"{test_module_name}/gradle.properties", 'r') as config_file:
        for line in config_file:
            try:
                fields = line.split("=")
                if len(fields) > 1:
                    name = fields[0]
                    value = "=".join(fields[1:])
                    if name in stdlib_module_versions.keys():
                        value = stdlib_module_versions[name] + "\n"
                    elif "ballerinaLangVersion" in name:
                        value = lang_version + "\n"
                    properties[name] = value
            except ValueError:
                continue
        config_file.close()

    with open(f"{test_module_name}/gradle.properties", 'w') as config_file:
        for prop in properties:
            config_file.write(prop + "=" + properties[prop])
        config_file.close()


def write_failed_modules(failed_module_names):
    with open("failed_modules.txt", "w") as file:
        for module_name in failed_module_names:
            file.write(module_name + "\n")
            print(f"Build failed for {module_name}")
        file.close()


def remove_dependency_files(module_name):
    if Path(module_name + "/ballerina/Dependencies.toml").is_file():
        os.system(f"cd {module_name}/ballerina;" +
                  "find . -name \"Dependencies.toml\" -delete;")

    elif module_name == "module-ballerinai-transaction" and \
            Path(module_name + "/transaction-ballerina/Dependencies.toml").is_file():
        os.system(f"cd {module_name}/transaction-ballerina;" +
                  "find . -name \"Dependencies.toml\" -delete;")

    if Path(module_name + "/ballerina-tests/Dependencies.toml").is_file():
        os.system(f"cd {module_name}/ballerina-tests;" +
                  "find . -name \"Dependencies.toml\" -delete;")


def delete_module(module_name):
    global exit_code

    exit_code = os.system(f"rm -rf ./{module_name}")
    if exit_code != 0:
        sys.exit(1)


main()
