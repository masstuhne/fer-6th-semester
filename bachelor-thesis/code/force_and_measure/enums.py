import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


class ATCommand:
    SIGNAL_QUALITY_MEASURE = config['at']['commands']['signal']['quality']
    OPERATOR_CURRENT = config['at']['commands']['operator']['current']
    OPERATOR_LIST = config['at']['commands']['operator']['list']
    OPERATOR_FORCE_A = config['at']['commands']['operator']['force']['automatic']
    OPERATOR_FORCE_M = config['at']['commands']['operator']['force']['manual']


class General:
    REGULAR_TIMEOUT = config['at']['timeout']['regular']
    SMALL_TIMEOUT = config['at']['timeout']['small']
    MEDIUM_TIMEOUT = config['at']['timeout']['medium']
    BIG_TIMEOUT = config['at']['timeout']['big']
    OUTPUT_FILE = config['file']['output']


class Serial:
    SERIAL_PORT = config['serial']['port']
    SERIAL_BAUDRATE = config['serial']['baudrate']


class Generation:
    HIGHER = 'higher'
    LOWER = 'lower'
    CURRENT = config['generation']
