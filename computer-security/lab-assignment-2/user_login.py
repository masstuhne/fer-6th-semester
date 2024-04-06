import sys
import re
import bcrypt
import database_commands
from getpass import getpass

strong_password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


def exit_program(message):
    sys.exit(message)


def handle_login(username):
    password = getpass('Password: ')
    password_bytes = password.encode('utf-8')

    if database_commands.exists_user_by_username(username):
        stored_password = database_commands.get_user_password(username)

        if bcrypt.checkpw(password_bytes, stored_password):
            should_force_reset_password = database_commands.get_user_force_req(username)
            if should_force_reset_password:
                handle_force_reset(username)
        else:
            exit_program('Invalid username or password!')
    else:
        exit_program('Invalid username or password!')

    exit_program('Successful login!')


def handle_force_reset(username):
    new_password = getpass("New Password: ")
    new_password_retype = getpass("Repeat New Password: ")

    if new_password != new_password_retype:
        exit_program("Password update failed. Password mismatch.")
    else:
        if re.search(strong_password_regex, new_password):
            new_password_bytes = new_password.encode("utf-8")
            new_hashed_password = bcrypt.hashpw(new_password_bytes, bcrypt.gensalt())
            database_commands.update_user_password(username, new_hashed_password)
            database_commands.update_user_force_req(username, False)
        else:
            exit_program("User add failed. Password is too weak.")


if __name__ == '__main__':
    cli_input = sys.argv
    if len(cli_input) != 2:
        exit_program('Usage not permitted!')
    else:
        username = cli_input[1]
        handle_login(username)
