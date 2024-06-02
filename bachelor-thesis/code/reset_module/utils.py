import time
from enums import General, ATCommand


def log_error(command):
    print(f'Error: {command}')


def send_at_command(ser, command, expected_response):
    ser.write((command + '\r\n').encode())
    print(f'Sent: {command}')

    time.sleep(General.REGULAR_TIMEOUT)

    response = ''
    if ser.inWaiting():
        time.sleep(General.SMALL_TIMEOUT)
        response = ser.read(ser.inWaiting()).decode()
    if expected_response not in response:
        log_error(command)
        return False
    else:
        return True
