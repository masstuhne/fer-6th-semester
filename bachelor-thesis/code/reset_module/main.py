import sys
import serial
from utils import *
from enums import Serial


def initialize_serial():
    port = Serial.SERIAL_PORT
    baudrate = Serial.SERIAL_BAUDRATE
    return serial.Serial(port, baudrate)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    ser = initialize_serial()
    try:
        success = send_at_command(ser, ATCommand.MODULE_DEFAULT_RESET, 'OK')
        if success:
            print('Module successfully reset!')
        else:
            print('Problem occurred while resetting the module!')
    except Exception as e:
        print(f'Error during reset: {e}')
        ser.close()
        return 1
    finally:
        print('Closing the serial port!')
        ser.close()
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
