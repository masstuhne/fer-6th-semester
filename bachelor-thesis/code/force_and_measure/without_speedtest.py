import serial
import time
import logging
import re
from enums import Serial, General, ATCommand, Generation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

access_technology_dict = {
    0: "GSM",
    1: "GSM Compact",
    2: "UTRAN",
    3: "EDGE",
    4: "HSDPA",
    5: "HSUPA",
    6: "HSDPA_HSUPA",
    7: "EUTRAN",
    8: "EC_GSM_IOT",
    9: "EUTRAN_NB_S1",
    10: "UTRAN_HSDPA",
    11: "NR_5GCN",
    12: "NGRAN",
    13: "EUTRA_NR"
}


class NetworkSwitcher:
    def __init__(self, port, baudrate, timeout, timeout_big):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.timeout_big = timeout_big
        self.serial_conn = None

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.info(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            # logger.error(f"Failed to connect to {self.port}: {e}")
            raise

    def send_at_command(self, command, timeout):
        try:
            self.serial_conn.write(f"{command}\r".encode())
            time.sleep(timeout)
            response = self.serial_conn.readlines()
            response_decoded = [line.decode().strip() for line in response]
            logger.info(f"Command '{command}' sent. Response: {response_decoded}")

            if any("OK" in line for line in response_decoded):
                return response_decoded
            elif any("ERROR" in line for line in response_decoded):
                logger.error(f"Command '{command}' returned an error.")
                return None
            else:
                logger.warning(f"Unexpected response for command '{command}': {response_decoded}")
                return None
        except serial.SerialException as e:
            logger.error(f"Error sending command '{command}': {e}")
            raise

    def check_current_network(self):
        logger.info("Checking current network...")
        response = self.send_at_command('AT+COPS?', self.timeout)
        current_network = self.parse_current_network_response(response)
        return current_network

    def parse_current_network_response(self, response):
        combined_response = ''.join(response)
        match = re.search(r'\+COPS: (\d),(\d),"(.+?)",(\d)', combined_response)
        if match:
            current_network = {
                'mode': int(match.group(1)),
                'format': int(match.group(2)),
                'oper': match.group(3),
                'tech': int(match.group(4))
            }
            logger.info(f"Current network: {current_network}")
            return current_network
        else:
            logger.warning("Failed to parse current network response.")
            return None

    def search_networks(self):
        logger.info("Searching for available networks...")
        response = self.send_at_command('AT+COPS=?', self.timeout_big)
        networks = self.parse_network_response(response)
        return networks

    def parse_network_response(self, response):
        networks = []
        combined_response = ''.join(response)
        matches = re.findall(r'\((\d+),"(.+?)","(.+?)","(\d+)",(\d+)\)', combined_response)
        for match in matches:
            network = {
                'status': int(match[0]),
                'name': match[1],
                'short_name': match[2],
                'mcc_mnc': match[3],
                'tech': int(match[4])
            }
            networks.append(network)
            logger.info(f"Found network: {network}")
        return networks

    def switch_network(self, target_generation='lower'):
        current_network = self.check_current_network()
        if not current_network:
            logger.error("Unable to determine current network. Aborting switch.")
            return

        current_tech = current_network['tech']
        networks = self.search_networks()

        if target_generation == 'lower':
            target_networks = [n for n in networks if n['tech'] < current_tech]
        else:
            target_networks = [n for n in networks if n['tech'] > current_tech]

        if not target_networks:
            logger.info(f"No {target_generation} generation networks available.")
            return

        selected_network = target_networks[0]
        mode = 1
        format = 2
        oper = selected_network['mcc_mnc']
        act = selected_network['tech']
        command = f'AT+COPS={mode},{format},"{oper}",{act}'
        self.send_at_command(command, self.timeout)
        logger.info(f"Switched to {target_generation} generation network: {selected_network['name']}")

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            logger.info(f"Connection to {self.port} closed.")


def main():
    port = Serial.SERIAL_PORT
    baudrate = Serial.SERIAL_BAUDRATE
    timeout = General.REGULAR_TIMEOUT
    timeout_big = General.BIG_TIMEOUT
    target_generation = Generation.LOWER
    check_interval = 60

    switcher = NetworkSwitcher(port, baudrate, timeout, timeout_big)
    try:
        switcher.connect()
        while True:
            switcher.switch_network(target_generation)
            time.sleep(check_interval)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        switcher.close()


if __name__ == "__main__":
    main()
