from json import dumps
from cryptography.fernet import Fernet
from httplib2 import Http
from github import Github
import os
import sys
import csv
import constants
import notify_chat

def main():
    ballerina_bot_token = os.environ[constants.ENV_BALLERINA_BOT_TOKEN]
    github = Github(ballerina_bot_token)
    repo = github.get_repo(constants.BALLERINA_ORG_NAME + '/' + "ballerina-distribution")

    message = "*Language server simulator failure in (" + str(sys.argv[0]) + ")*" + \
              "Please visit the <https://github.com/ballerina-platform/ballerina-distribution/actions/runs/" + \
              + str(sys.argv[1]) + "|the LS simulator run>" + \
              "for more information\n"

    try:
        owners = ["gimantha","KavinduZoysa"]
        encryption_key = os.environ['ENV_USER_ENCRYPTION_KEY']

        fernet = Fernet(encryption_key)
        with open('dependabot/resources/github_users_encrypted.csv', 'rb') as enc_file:
            encrypted_csv = enc_file.read()

        decrypted = fernet.decrypt(encrypted_csv)
        with open('dependabot/resources/github_users_decrypted.csv', 'wb') as dec_file:
            dec_file.write(decrypted)

        for owner in owners:
            with open('dependabot/resources/github_users_decrypted.csv', 'r') as read_obj:
                user_file = csv.DictReader(read_obj)
                owner = owner.strip()
                for row in user_file:
                    if row['gh-username'] == owner:
                        message += "<users/" + row['user-id'] + ">" + "\n"

        notify_chat.send_message(message)
    except:
        notify_chat.send_message(message)

main()
