import csv
import serial
import time
from datetime import datetime


responses = []
responses_times = []
cell_ids = []
cell_ids_times = []


def write_data(data_1, data_2, data_3, data_4, output_file):
    combined_data = []

    for (lat_lon, lac_ci, time_1, time_2) in zip(data_1, data_2, data_3, data_4):
        lat, lon = lat_lon
        lac, ci = lac_ci

        time1 = datetime.strptime(time_1, '%Y-%m-%d %H:%M:%S.%f')
        time2 = datetime.strptime(time_2, '%Y-%m-%d %H:%M:%S.%f')

        print(time1)
        print(time2)
        print("----")
        
        time_difference_microseconds = (time2 - time1).total_seconds() * 1e6

        combined_row = [lat, lon, lac, ci, time_difference_microseconds]
        combined_data.append(combined_row)

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Latitude', 'Longitude', 'LAC', 'CI', 'Time_error'])
        writer.writerows(combined_data)
    
    print(f'Data successfully written to {output_file}')



def parse_responses(responses):
    data = []

    for response in responses:
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


def parse_cell_ids(cell_ids):
    data = []

    for response in cell_ids:
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
    

def send_at_command(ser, timeout, command, expected_response):
    ser.write((command + '\r\n').encode())        

    time.sleep(timeout)
    
    response = ''
    if ser.inWaiting():
            time.sleep(0.01)
            response = ser.read(ser.inWaiting()).decode()
    if  expected_response not in response:
        print(command + ' ERROR')
        return False
    else:
        current_time_microseconds = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if command == 'AT+CGPSINFO':
            responses.append(response)
            responses_times.append(current_time_microseconds)
        elif command == 'AT+CREG?':
            cell_ids.append(response)
            cell_ids_times.append(current_time_microseconds)
        return True


def run():
    ser = serial.Serial('/dev/ttyUSB2', 115200)
    try:
        success = send_at_command(ser, 1, 'AT+CGPS=1', 'OK')
        if not success:
            send_at_command(ser, 1, 'AT+CGPS=0', 'OK')
            ser.close()
        success = send_at_command(ser, 1, 'AT+CREG=2', 'OK')
        if not success:
            ser.close()
    except:
        ser.close()

    i = 0
    while(i < 10):
        try:
            success = send_at_command(ser, 0.5, 'AT+CGPSINFO', 'OK')
            success = send_at_command(ser, 0.5, 'AT+CREG?', 'OK')
        except:
            ser.close()
        i += 1
    
    data_1 = parse_responses(responses)
    data_2 = parse_cell_ids(cell_ids)
    write_data(data_1, data_2, responses_times, cell_ids_times ,"output.txt")
    print('Closing the serial port!')
    ser.close()

if __name__ == '__main__':
    run()