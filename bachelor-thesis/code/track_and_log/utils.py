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


def send_at_command(ser, command, expected_response, gps_response,
                    gps_time, cell_response, cell_time):
    ser.write((command + '\r\n').encode())
    print(f'Sent: {command}')

    time.sleep(General.REGULAR_TIMEOUT)

    response = ''
    if ser.inWaiting():
        time.sleep(General.SMALL_TIMEOUT)
        response = ser.read(ser.inWaiting()).decode()
    if expected_response not in response:
        log_error(command)
        return False
    else:
        current_time_microseconds = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if command == ATCommand.GPS_POSITION_INFO:
            gps_response.append(response)
            gps_time.append(current_time_microseconds)
        elif command == ATCommand.CREG_STATUS_INFO:
            cell_response.append(response)
            cell_time.append(current_time_microseconds)
        return True
