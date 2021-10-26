from json import dumps
from cryptography.fernet import Fernet
from httplib2 import Http
import os
import sys
import csv

def main()
    code_owners = open("CODEOWNERS", "r")
    owners = code_owners.read().split("*")[1].split("@")

    encryption_key = os.environ['ENV_USER_ENCRYPTION_KEY']

    fernet = Fernet(encryption_key)
    with open('dependabot/resources/github_users_encrypted.csv', 'rb') as enc_file:
        encrypted_csv = enc_file.read()

    decrypted = fernet.decrypt(encrypted_csv)
    with open('dependabot/resources/github_users_decrypted.csv', 'wb') as dec_file:
        dec_file.write(decrypted)

    message = "*" + str(sys.argv[1]) + "* daily build failure" + "\n" +\
              "Please visit <https://github.com/ballerina-platform/" + str(sys.argv[1]) + "/actions?query=workflow%3A%22Daily+build%22|the daily build page> for more information" +"\n"

    for owner in owners :
        with open('dependabot/resources/github_users_decrypted.csv', 'r') as read_obj:
            user_file = csv.DictReader(read_obj)
            owner = owner.strip()
            for row in user_file:
                if row['gh-username'] == owner:
                    message += "<users/" + row['user-id'] + ">" + "\n"

    build_chat_id = os.environ['ENV_NOTIFICATIONS_CHAT_ID']
    build_chat_key = os.environ['ENV_NOTIFICATIONS_CHAT_KEY']
    build_chat_token = os.environ['ENV_NOTIFICATIONS_CHAT_TOKEN']

    url = 'https://chat.googleapis.com/v1/spaces/' + build_chat_id + \
              '/messages?key=' + build_chat_key + '&token=' + build_chat_token

    chat_message = {"text": message}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    resp = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(chat_message)
    )[0]

    if resp.status == 200:
        print("Successfully sent notification")
    else:
        print("Failed to send notification, status code: " + str(resp.status))
        sys.exit(1)

main()
