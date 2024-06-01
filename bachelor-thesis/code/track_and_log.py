import serial
import time

class Commands:

def send_at_command(ser, timeout, command):
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    response = ser.read()


def run():
    ser = serial.Serial('/dev/ttyUSB2', 115200)
    try:


if __name__ == '__main__':
    run()