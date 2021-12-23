import json
import requests
import constants
import os
import sys
import urllib.request


stdlib_modules_json_file_url = 'https://raw.githubusercontent.com/ballerina-platform/ballerina-standard-library/' \
                               'main/release/resources/stdlib_modules.json'
properties_file_url = "https://raw.githubusercontent.com/ballerina-platform/ballerina-distribution/master/gradle.properties"

release_version = ""
exit_code = 0

stdlib_module_versions = dict()

ballerina_bot_username = os.environ[constants.ENV_BALLERINA_BOT_USERNAME]
ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]


def main():
    global stdlib_modules_json_file_url
    global release_version
    global properties_file_url

    if len(sys.argv) > 1:
        release_version = sys.argv[1]
        properties_file_url = "https://raw.githubusercontent.com/ballerina-platform/ballerina-distribution/v" + \
                          release_version + "/gradle.properties"

    read_stdlib_version()

    clone_repositories()

    push_stdlibs_to_dev_central()
    push_stdlibs_to_stage_central()


def read_stdlib_version():
    try:
        response = requests.get(url=stdlib_modules_json_file_url)

        if response.status_code == 200:
            stdlib_modules_data = json.loads(response.text)
            read_version_data(stdlib_modules_data)
        else:
            print('Failed to access standard library dependency data from', stdlib_modules_json_file_url)
            sys.exit(1)

    except json.decoder.JSONDecodeError:
        print('Failed to load standard library dependency data')
        sys.exit(1)


def read_version_data(stdlib_modules_data):
    global stdlib_module_versions

    try:
        req = urllib.request.Request(properties_file_url)

        properties = dict()
        for line in urllib.request.urlopen(req):
            line = line.decode("utf-8")
            if "=" in line:
                name, value = line.strip().split("=")
                properties[name] = value

    except:
        print('Failed to load properties from', properties_file_url)
        sys.exit(1)

    for module in stdlib_modules_data['modules']:
        name = module['name']
        version_key = module['version_key']
        try:
            stdlib_module_versions[name] = properties[version_key]
        except KeyError:
            if "ballerinax" not in name and "ballerinai" not in name:
                print('Version key', version_key, 'not found in', properties_file_url)
                sys.exit(1)


def clone_repositories():
    global exit_code

    # Clone standard library repos
    for module in stdlib_module_versions:
        print(f"git clone -b v{stdlib_module_versions[module]} {constants.BALLERINA_ORG_URL}{module}.git")
        exit_code = os.system(f"git clone -b v{stdlib_module_versions[module]} {constants.BALLERINA_ORG_URL}{module}.git")
        if exit_code != 0:
            sys.exit(1)


def push_stdlibs_to_dev_central():
    global exit_code

    # Build standard library repos and push dev central
    for module in stdlib_module_versions:
        os.system(f"echo Building Standard Library Module: {module}")
        exit_code = os.system(f"cd {module}/ballerina;" +
                              f"export packageUser={ballerina_bot_username};" +
                              f"export packagePAT={ballerina_bot_token};" +
                              f"export BALLERINA_DEV_CENTRAL=true;" +
                              f"export BALLERINA_STAGE_CENTRAL=false;" +
                              f"bal build;bal pack;bal push")
        if exit_code != 0:
            print(f"Build failed for {module}")
            sys.exit(1)


def push_stdlibs_to_stage_central():
    global exit_code

    # Build standard library repos and push stage central
    for module in stdlib_module_versions:
        os.system(f"echo Building Standard Library Module: {module}")
        exit_code = os.system(f"cd {module}/ballerina;" +
                              f"export packageUser={ballerina_bot_username};" +
                              f"export packagePAT={ballerina_bot_token};" +
                              f"export BALLERINA_DEV_CENTRAL=false;" +
                              f"export BALLERINA_STAGE_CENTRAL=true;" +
                              f"bal build;bal pack;bal push")
        if exit_code != 0:
            print(f"Build failed for {module}")
            sys.exit(1)


main()
