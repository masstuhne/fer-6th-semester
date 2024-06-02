import re
import csv
import time
from enums import ATCommand, General
from datetime import datetime


def log_error(command):
    print(f'Error: {command}')


def write_to_csv(gps_data, cell_data, gps_call_time, cell_call_time, output_file):
    combined_data = []

    data_zip = zip(gps_data, cell_data, gps_call_time, cell_call_time)
    for (lat_lon, lac_ci, gps_time, cell_time) in data_zip:
        lat, lon = lat_lon
        lac, ci = lac_ci

        time1 = datetime.strptime(gps_time, '%Y-%m-%d %H:%M:%S.%f')
        time2 = datetime.strptime(cell_time, '%Y-%m-%d %H:%M:%S.%f')

        time_difference_microseconds = (time2 - time1).total_seconds() * 1e6

        combined_row = [lat, lon, lac, ci, time_difference_microseconds]
        combined_data.append(combined_row)

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Latitude', 'Longitude', 'LAC', 'CI', 'Time_error'])
        writer.writerows(combined_data)

    print(f'Data successfully written to {output_file}')


def parse_current_operator(response):
    format = ''
    operator = ''
    technology = ''

    lines = response.splt('\n')
    for line in lines:
        if ',' in line:
            parts = line.split(':')[1].strip().split(',')
            format = parts[1].strip()
            operator = parts[2].strip()
            technology = parts[3].strip()

    return format, operator, technology


def parse_operator_list(response):
    pattern = re.compile(r'\((\d+),"([^"]*)","([^"]*)","(\d+)",(\d+)\)')

    supported = pattern.findall(response)
    operator_list = [(int(s[0]), s[1], s[2], s[3], int(s[4])) for s in supported]
    return operator_list


def parse_gps_response(response_list):
    data = []

    for response in response_list:
        lines = response.split('\n')

        for line in lines:
            if ',' in line:
                parts = line.split(':')[1].strip().split(',')
                if len(parts) >= 3:
                    lat = parts[0].strip()
                    lon = parts[2].strip()

                    if lat and lon:
                        data.append([lat, lon])
                    else:
                        data.append(['ERR', 'ERR'])
    return data


def parse_creg_response(response_list):
    data = []

    for response in response_list:
        lines = response.split('\n')

        for line in lines:
            if ',' in line:
                parts = line.split(':')[1].strip().split(',')
                if len(parts) == 4:
                    lac = parts[2].strip()
                    ci = parts[3].strip()

                    if lac and ci:
                        data.append([lac, ci])
                    else:
                        data.append(['ERR', 'ERR'])
    return data


def send_at_command(ser, command, expected_response):
    ser.write((command + '\r\n').encode())
    print(f'Sent: {command}')

    if command == ATCommand.OPERATOR_LIST or command == ATCommand.OPERATOR_FORCE_M:
        time.sleep(General.BIG_TIMEOUT)
    else:
        time.sleep(General.REGULAR_TIMEOUT)

    response = ''
    if ser.inWaiting():
        time.sleep(General.SMALL_TIMEOUT)
        response = ser.read(ser.inWaiting()).decode()
    if expected_response not in response:
        log_error(command)
        return False, None
    else:
        return True, response
