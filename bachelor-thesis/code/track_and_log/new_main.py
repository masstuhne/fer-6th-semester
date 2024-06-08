import serial
import time
import logging
import re
import csv
import os
from enums import Serial, General, ATCommand

# Configure logging with timestamps
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Access Technology Dictionary
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


class GPSLogger:
    def __init__(self, port, baudrate, timeout, log_additional_info=False, csv_filename='gps_log.csv'):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.log_additional_info = log_additional_info
        self.csv_filename = csv_filename
        self.mnc = None
        self.mcc = None

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.info(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            logger.error(f"Failed to connect to {self.port}: {e}")
            raise

    def send_at_command(self, command):
        try:
            self.serial_conn.write(f"{command}\r".encode())
            time.sleep(self.timeout)  # Wait for the command to be processed
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

    def get_mnc_mcc(self):
        logger.info("Getting MNC and MCC...")
        response = self.send_at_command('AT+COPS?')
        if response:
            combined_response = ''.join(response)
            match = re.search(r'\+COPS: \d,\d,"(.+?)",\d', combined_response)
            if match:
                mcc_mnc = match.group(1)
                self.mcc, self.mnc = mcc_mnc[:3], mcc_mnc[3:]
                logger.info(f"Retrieved MNC: {self.mnc}, MCC: {self.mcc}")
            else:
                logger.warning("Failed to parse MNC and MCC response.")
        else:
            logger.error("Failed to get MNC and MCC.")

    def start_gps_session(self):
        logger.info("Starting GPS session...")
        self.send_at_command('AT+CGPS=1')

    def get_gps_info(self):
        logger.info("Getting GPS information...")
        response = self.send_at_command('AT+CGPSINFO?')
        if response:
            combined_response = ''.join(response)
            match = re.search(r'\+CGPSINFO: (.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)', combined_response)
            if match:
                gps_info = {
                    'latitude': match.group(1),
                    'latitude_direction': match.group(2),
                    'longitude': match.group(3),
                    'longitude_direction': match.group(4),
                    'date': match.group(5),
                    'utc_time': match.group(6),
                    'altitude': match.group(7),
                    'speed': match.group(8),
                    'course': match.group(9)
                }
                logger.info(f"GPS Information: {gps_info}")
                return gps_info
            else:
                logger.warning("Failed to parse GPS information.")
                return None
        else:
            logger.error("Failed to get GPS information.")
            return None

    def get_lac_ci(self):
        logger.info("Getting LAC and CI...")
        response = self.send_at_command('AT+CREG?')
        if response:
            combined_response = ''.join(response)
            match = re.search(r'\+CREG: \d,(\d+),"(.*?)","(.*?)"', combined_response)
            if match:
                lac = match.group(2)
                ci = match.group(3)
                logger.info(f"LAC: {lac}, CI: {ci}")
                return lac, ci
            else:
                logger.warning("Failed to parse LAC and CI information.")
                return None, None
        else:
            logger.error("Failed to get LAC and CI.")
            return None, None

    def log_signal_quality(self):
        logger.info("Checking signal quality...")
        response = self.send_at_command('AT+CSQ')
        if response:
            combined_response = ''.join(response)
            match = re.search(r'\+CSQ: (\d+),(\d+)', combined_response)
            if match:
                rssi = int(match.group(1))
                ber = int(match.group(2))
                logger.info(f"Signal Quality - RSSI: {rssi}, BER: {ber}")
                return rssi, ber
            else:
                logger.warning("Failed to parse signal quality response.")
                return None, None
        else:
            logger.error("Failed to get signal quality.")
            return None, None

    def log_current_technology(self):
        logger.info("Checking current technology...")
        response = self.send_at_command('AT+COPS?')
        if response:
            combined_response = ''.join(response)
            match = re.search(r'\+COPS: \d,\d,".*?",(\d)', combined_response)
            if match:
                tech = int(match.group(1))
                technology = access_technology_dict.get(tech, "Unknown")
                logger.info(f"Current Technology: {technology}")
                return technology
            else:
                logger.warning("Failed to parse current technology response.")
                return "Unknown"
        else:
            logger.error("Failed to get current technology.")
            return "Unknown"

    def write_to_csv(self, data):
        file_exists = os.path.isfile(self.csv_filename)
        with open(self.csv_filename, 'a', newline='') as csvfile:
            fieldnames = [
                'latitude', 'latitude_direction', 'longitude', 'longitude_direction', 'date', 'utc_time',
                'altitude', 'speed', 'course', 'lac', 'ci', 'mnc', 'mcc', 'rssi', 'ber', 'technology'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            logger.info(f"Connection to {self.port} closed.")


def main():
    port = Serial.SERIAL_PORT
    baudrate = Serial.SERIAL_BAUDRATE
    timeout = General.REGULAR_TIMEOUT
    log_additional_info = True  # Set to True to log additional info like current technology or signal quality
    check_interval = 1  # Time in seconds between checks

    gps_logger = GPSLogger(port, baudrate, timeout,log_additional_info=log_additional_info)
    try:
        gps_logger.connect()
        gps_logger.get_mnc_mcc()
        gps_logger.start_gps_session()
        while True:
            gps_info = gps_logger.get_gps_info() or {}
            lac, ci = gps_logger.get_lac_ci()
            rssi, ber = (None, None)
            technology = "Unknown"
            if log_additional_info:
                rssi, ber = gps_logger.log_signal_quality()
                technology = gps_logger.log_current_technology()

            data = {
                'latitude': gps_info.get('latitude'),
                'latitude_direction': gps_info.get('latitude_direction'),
                'longitude': gps_info.get('longitude'),
                'longitude_direction': gps_info.get('longitude_direction'),
                'date': gps_info.get('date'),
                'utc_time': gps_info.get('utc_time'),
                'altitude': gps_info.get('altitude'),
                'speed': gps_info.get('speed'),
                'course': gps_info.get('course'),
                'lac': lac,
                'ci': ci,
                'mnc': gps_logger.mnc,
                'mcc': gps_logger.mcc,
                'rssi': rssi,
                'ber': ber,
                'technology': technology
            }
            gps_logger.write_to_csv(data)
            time.sleep(check_interval)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        gps_logger.close()


if __name__ == "__main__":
    main()
