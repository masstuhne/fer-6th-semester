import sys
import re
import bcrypt
import uuid
import database_commands
from getpass import getpass

strong_password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


def exit_program(message):
    sys.exit(message)


def handle_add(username):
    # password = getpass("Password: ")
    password = input("Password: \n")
    # password_retype = getpass("Repeat Password: ")
    password_retype = input("Repeat Password: \n")


    if password != password_retype:
        exit_program("User add failed. Password mismatch.")
    else:
        if database_commands.exists_user_by_username(str(username)):
            exit_program("User add failed. User already exists.")
        else:
            if re.search(strong_password_regex, password):
                password_bytes = password.encode("utf-8")
                hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
                database_commands.add_user(str(uuid.uuid4()), str(username), hashed_password, False)
            else:
                exit_program("User add failed. Password is too weak.")


def handle_update_password(username):
    # password = getpass("Password: ")
    password = input("Password: \n")
    # password_retype = getpass("Repeat Password: ")
    password_retype = input("Repeat Password: \n")

    if password != password_retype:
        exit_program("Password update failed. Password mismatch.")
    else:
        if not database_commands.exists_user_by_username(username):
            exit_program("User add failed. User does not exists.")
        else:
            if re.search(strong_password_regex, password):
                password_bytes = password.encode("utf-8")
                hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
                database_commands.update_user_password(username, hashed_password)
            else:
                exit_program("User add failed. Password is too weak.")


def handle_update_force_req(username, force_req):
    if not database_commands.exists_user_by_username(username):
        exit_program("Force password change failed. User does not exists.")
    database_commands.update_user_force_req(username, force_req)


def handle_delete(username):
    if not database_commands.exists_user_by_username(username):
        exit_program("User delete failed. User does not exists.")
    database_commands.delete_user(username)


if __name__ == '__main__':
    cli_input = sys.argv
    if len(cli_input) != 3:
        exit_program('Usage not permitted!')
    else:
        action = cli_input[1]
        username = cli_input[2]
        if action.__eq__('add'):
            handle_add(username)
        elif action.__eq__('passwd'):
            handle_update_password(username)
        elif action.__eq__('forcepass'):
            handle_update_force_req(username, True)
        elif action.__eq__('del'):
            handle_delete(username)
        else:
            exit_program('Action not permitted!')
