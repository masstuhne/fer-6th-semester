import sys
import serial
from utils import *
from enums import ATCommand, General, Serial


def initialize_serial():
    port = Serial.SERIAL_PORT
    baudrate = Serial.SERIAL_BAUDRATE
    return serial.Serial(port, baudrate)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    gps_response = []
    gps_response_times = []
    creg_response = []
    creg_response_times = []

    ser = initialize_serial()
    try:
        if not send_at_command(ser, ATCommand.GPS_SESSION_START, 'OK',
                               gps_response, gps_response_times,
                               creg_response, creg_response_times):
            send_at_command(ser, ATCommand.GPS_SESSION_STOP, 'OK',
                            gps_response, gps_response_times,
                            creg_response, creg_response_times)
            ser.close()
            return 0
        if not send_at_command(ser, ATCommand.CREG_MORE_INFO, 'OK',
                               gps_response, gps_response_times,
                               creg_response, creg_response_times):
            ser.close()
            return 0
    except Exception as e:
        print(f'Error during initialization: {e}')
        ser.close()
        return 1

    for _ in range(10):
        try:
            send_at_command(ser, ATCommand.GPS_POSITION_INFO, 'OK',
                            gps_response, gps_response_times,
                            creg_response, creg_response_times)
            send_at_command(ser, ATCommand.CREG_STATUS_INFO, 'OK',
                            gps_response, gps_response_times,
                            creg_response, creg_response_times)
        except Exception as e:
            print(f'Error during command sending: {e}')
            ser.close()
            return 1

    gps_data = parse_gps_response(gps_response)
    cell_data = parse_creg_response(creg_response)
    write_to_csv(gps_data, cell_data, gps_response_times, creg_response_times, General.OUTPUT_FILE)

    print('Closing the serial port!')
    ser.close()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
