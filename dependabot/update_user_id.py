import csv
import os
import sys

from github import Github
from cryptography.fernet import Fernet

import utils
import constants
encryption_key = os.environ['ENV_USER_ENCRYPTION_KEY']
fernet = Fernet( encryption_key )

def main():
    with open('dependabot/resources/github_users_encrypted.csv', 'rb') as enc_file:
        encrypted_csv = enc_file.read()

    decrypted = fernet.decrypt(encrypted_csv)
    with open('dependabot/resources/github_users_decrypted.csv', 'wb') as dec_file:
        dec_file.write(decrypted)

    if str(sys.argv[5]) == "a":
        if str(sys.argv[3]) == "" or str( sys.argv[4]) == "":
            print( "Missing required fields for adding")
        else:
            add_field( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )
            committed = commit_notify_work()
            if committed:
                utils.open_pr_and_merge('ballerina-release',
                                        '[Automated] Add an userid field',
                                        'Add new userid to the encrypted csv',
                                        constants.USERID_UPDATE_BRANCH )
            else:
                print('No changes to the encrypted csv file')
    elif str(sys.argv[5]) == "r":
        remove_field(sys.argv[1], sys.argv[2])
        committed = commit_notify_work()
        if committed:
            utils.open_pr_and_merge( 'ballerina-release',
                                     '[Automated] Remove an userid field ',
                                     'Remove a userid from encrypted csv',
                                     constants.USERID_UPDATE_BRANCH )
        else:
            print('No changes to the encrypted csv file')
    else:
        print( "Invalid operation")


def add_field( github_username, org_id, user_id, team_name):
    with open('dependabot/resources/github_users_decrypted.csv', 'a') as write_obj:
        field_names = ['gh-username','wso2-id','user-id','team']
        user_file = csv.DictWriter(write_obj , fieldnames = field_names)
        user_file.writerow({'gh-username': github_username, 'wso2-id': org_id, 'user-id': user_id, 'team': team_name})
        write_obj.close()

    ## Encrypt the updated csv
    with open('dependabot/resources/github_users_decrypted.csv', 'rb') as file:
        updated_csv_file = file.read()
    encrypted = fernet.encrypt(updated_csv_file)

    with open('file_to_commit.csv', 'wb') as encrypt_obj:
        encrypt_obj.write(encrypted)


def remove_field( github_username, org_id ):
    lines = []
    with open('dependabot/resources/github_users_decrypted.csv', 'rb') as read_obj:
        user_file = csv.reader(read_obj)
        for row in user_file:
            lines.append(row)
            if row[0] == github_username and row[1] == org_id:
                lines.remove(row)

    with open('dependabot/resources/updated.csv', 'wb') as write_obj:
        writer = csv.writer(write_obj)
        writer.writerows(lines)

    ## Encrypt the updated csv
    with open('dependabot/resources/updated.csv', 'rb') as file:
        updated_csv_file = file.read()
    encrypted = fernet.encrypt(updated_csv_file)

    with open('file_to_commit.csv', 'wb') as encrypt_obj:
        encrypt_obj.write(encrypted)


def commit_notify_work():
    with open('file_to_commit.csv', 'r') as enc_file:
        updated_file_content = enc_file.read()
    update = utils.commit_file('ballerina-release',
                                'dependabot/resources/github_users_encrypted.csv',
                                updated_file_content,
                                constants.USERID_UPDATE_BRANCH,
                                "[Automated] Update userid file")[0]
    return update

main()
