import sys
import serial
from utils import *
from enums import General, ATCommand, Serial, Generation


access_technology_dict = {
    "GSM": 0,
    "GSM Compact": 1,
    "UTRAN": 2,
    "UTRAN_HSDPA_HSUPA": 6,
    "EUTRAN": 7,
    "EC_GSM_IOT": 8,
    "EUTRAN_NB_S1": 9,
    "NR_5GCN": 11,
    "NGRAN": 12,
    "EUTRA_NR": 13
}


def initialize_serial():
    port = Serial.SERIAL_PORT
    baudrate = Serial.SERIAL_BAUDRATE
    return serial.Serial(port, baudrate)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    curr_format = ''
    curr_operator = ''
    curr_technology = ''

    prefered_mode = Generation.CURRENT

    ser = initialize_serial()
    try:
        success, response = send_at_command(ser, ATCommand.OPERATOR_CURRENT, 'OK')
        curr_format, curr_operator, curr_technology = parse_current_operator(response)
        if not success:
            print('Problem occurred while getting the current operator')
            ser.close()
            return 0
    except Exception as e:
        print(f'Error during initialization: {e}')
        ser.close()
        return 1

    try:
        success, response = send_at_command(ser, ATCommand.OPERATOR_LIST, 'OK')
        operator_list = parse_operator_list(response)
        if not success:
            print('Problem occurred while getting the operator list')
            ser.close()
            return 0
    except Exception as e:
        print(f'Error during initialization: {e}')
        ser.close()
        return 1

    for operator in operator_list:
        operator_technology_number = operator[4]
        operator_numeric = operator[3]
        command = ATCommand.OPERATOR_FORCE_M + str(operator_numeric) + str(operator_technology_number)
        if prefered_mode == Generation.HIGHER:
            if operator_technology_number > curr_technology:
                success, response = send_at_command(ser, command, 'OK')
                if success:
                    curr_technology = operator_technology_number
                    print('Operator changed successfully')
                else:
                    print('Problem occurred while changing operators')
        else:
            if operator_technology_number < curr_technology:
                success, response = send_at_command(ser, command, 'OK')
                if success:
                    curr_technology = operator_technology_number
                    print('Operator changed successfully')
                else:
                    print('Problem occurred while changing operators')

    try:
        success, response = send_at_command(ser, ATCommand.OPERATOR_CURRENT, 'OK')
        curr_format, curr_operator, curr_technology = parse_current_operator(response)
        if not success:
            print('Problem occurred while getting the current operator')
            ser.close()
            return 0
    except Exception as e:
        print(f'Error during initialization: {e}')
        ser.close()
        return 1
    finally:
        print(curr_format + ' ' + curr_operator + ' ' + curr_technology)
        print('Closing the serial port!')
        ser.close()
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
