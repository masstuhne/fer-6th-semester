import os
import sys

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

SALT_LENGTH = 16
NONCE_LENGTH = 16
TAG_LENGTH = 16

database_file = 'database_file.bin'


def exit_program(message):
    sys.exit(message)


def generate_key(master_password):
    salt = get_random_bytes(SALT_LENGTH)
    key = scrypt(master_password, str(salt), 16, 2 ** 14, 8, 1)
    return key, salt


def handle_init(master_password):
    global database_file

    # with automatically closes the file
    # with open('database_file.bin', 'wb'):
    #     pass
    encrypt('', master_password)
    print('Password manager initialized.')


def handle_put(master_password, website, password):
    global database_file
    information_bytes, success = decrypt(master_password)

    if success:
        new_information = ''
        password_dictionary = {}
        information = information_bytes.decode('utf-8')

        for line in information:
            line_website, line_password = line.split(' ')
            password_dictionary.update({line_website: line_password})

        password_dictionary.update({website: password})
        for key_website, value_password in password_dictionary.items():
            new_information += key_website
            new_information += ' '
            new_information += password
            new_information += '\n'
        new_information.rstrip('\n')

        new_information_bytes = new_information.encode('utf-8')

        encrypt(new_information_bytes, master_password)

        print(f'Stored password for {website}')
    else:
        exit_program('Master password incorrect or integrity check failed.')


def handle_get(master_password, website):
    information_bytes, success = decrypt(master_password)
    found = False
    result = ''

    if success:
        information = information_bytes.decode('utf-8')

        # for line in information:
        #     print(line)
        line_website, line_password = information.split(' ')
        if line_website.__eq__(website):
            found = True
            result = line_password

        if found:
            print(f'Password for {website} is: {result}')
        else:
            print(f'No password found for: {website}')
    else:
        exit_program('Master password incorrect or integrity check failed.')


def get_database_bytes():
    file_size = os.path.getsize(database_file)
    with open('database_file.bin', 'rb') as db_file:
        salt = db_file.read(SALT_LENGTH)
        nonce = db_file.read(NONCE_LENGTH)
        information = db_file.read(file_size - SALT_LENGTH - NONCE_LENGTH - TAG_LENGTH)
        tag = db_file.read(TAG_LENGTH)
    return salt, nonce, information, tag


def encrypt(text, master_password):
    key, salt = generate_key(master_password)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    cipher_text = ''

    if text:
        cipher_text = cipher.encrypt(text)

    tag = cipher.digest()

    with open('database_file.bin', 'wb') as db_file:
        db_file.write(salt)
        db_file.write(nonce)
        if cipher_text:
            db_file.write(cipher_text)
        db_file.write(tag)


def decrypt(master_password):
    salt, nonce, information, tag = get_database_bytes()

    key = scrypt(master_password, str(salt), 16, 2 ** 14, 8, 1)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        information_decrypted = cipher.decrypt_and_verify(information, tag)
    except ValueError as err:
        return b'', False
    return information_decrypted, True


if __name__ == '__main__':
    cli_input = sys.argv
    if len(cli_input) != 3 and len(cli_input) != 4 and len(cli_input) != 5:
        exit_program('Usage not permitted!')
    else:
        action = cli_input[1]
        master_password = cli_input[2]
        if action.__eq__('init'):
            handle_init(master_password)
        elif action.__eq__('put'):
            website = cli_input[3]
            password = cli_input[4]
            handle_put(master_password, website, password)
        elif action.__eq__('get'):
            website = cli_input[3]
            handle_get(master_password, website)
        else:
            exit_program('Action not permitted!')
