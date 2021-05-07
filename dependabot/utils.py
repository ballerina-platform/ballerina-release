import json
import urllib.request

from retry import retry

import constants


def get_extensions_file():
    try:
        with open(constants.EXTENSIONS_FILE) as f:
            module_list = json.load(f)
    except Exception as e:
        raise e

    return module_list


@retry(
    urllib.error.URLError,
    tries=constants.HTTP_REQUEST_RETRIES,
    delay=constants.HTTP_REQUEST_DELAY_IN_SECONDS,
    backoff=constants.HTTP_REQUEST_DELAY_MULTIPLIER
)
def open_url(url, auth_token):
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github.v3+json")
    request.add_header("Authorization", "Bearer " + auth_token)

    return urllib.request.urlopen(request)


def get_latest_lang_version(auth_token):
    try:
        version_string = open_url(
            "https://api.github.com/orgs/ballerina-platform/packages/maven/org.ballerinalang.jballerina-tools/versions",
            auth_token).read()
    except Exception as e:
        raise e

    versions_list = json.loads(version_string)
    latest_version = versions_list[0]['name']

    extensions_file = get_extensions_file()

    if extensions_file['lang_version_regex'] != "":
        for version in versions_list:
            version_name = version['name']
            if extensions_file['lang_version_regex'] in version_name:
                latest_version = version_name
                break
    return latest_version
