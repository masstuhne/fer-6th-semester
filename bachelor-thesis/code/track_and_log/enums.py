import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


class ATCommand:
    GPS_SESSION_START = config['at']['commands']['gps']['enable']
    GPS_SESSION_STOP = config['at']['commands']['gps']['disable']
    GPS_POSITION_INFO = config['at']['commands']['gps']['info']
    CREG_MORE_INFO = config['at']['commands']['registration']['info']['more']
    CREG_LESS_INFO = config['at']['commands']['registration']['info']['less']
    CREG_STATUS_INFO = config['at']['commands']['registration']['info']['status']


class General:
    REGULAR_TIMEOUT = config['at']['timeout']['regular']
    SMALL_TIMEOUT = config['at']['timeout']['small']
    OUTPUT_FILE = config['file']['output']


class Serial:
    SERIAL_PORT = config['serial']['port']
    SERIAL_BAUDRATE = config['serial']['baudrate']
