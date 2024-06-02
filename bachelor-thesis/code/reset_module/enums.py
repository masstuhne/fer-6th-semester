import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


class ATCommand:
    MODULE_DEFAULT_RESET = config['at']['commands']['reset']


class General:
    REGULAR_TIMEOUT = config['at']['timeout']['regular']
    SMALL_TIMEOUT = config['at']['timeout']['small']


class Serial:
    SERIAL_PORT = config['serial']['port']
    SERIAL_BAUDRATE = config['serial']['baudrate']
