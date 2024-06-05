import sys
import re


def handle_error(message):
    print(message)
    sys.exit(1)


def analyze_logfile(logfile, resource):
    try:
        with open(logfile, 'r') as file:
            log_data = file.readlines()
    except FileNotFoundError:
        handle_error(f'Error: The file {logfile} does not exist.')

    ip_pattern = re.compile(r'(\d+\.\d+)\.\d+\.\d+')
    request_pattern = re.compile(r'\"[A-Z]+\s(' + re.escape(resource) + r')\sHTTP/1\.[01]\"')

    subnet_access_count = {}

    for log in log_data:
        ip_match = ip_pattern.search(log)
        request_match = request_pattern.search(log)

        if ip_match and request_match:
            subnet = ip_match.group(1)
            if subnet not in subnet_access_count:
                subnet_access_count[subnet] = 1
            else:
                subnet_access_count[subnet] += 1

    filtered_subnets = [(subnet, count) for subnet, count in subnet_access_count.items() if count >= 2]
    sorted_subnets = sorted(filtered_subnets, key=lambda x: x[1], reverse=True)

    print('-------------------------------------------')
    print(f'Broj pristupa stranici: {resource}')
    print('  IP podmreza : Broj pristupa')
    print('-------------------------------------------')
    for subnet, access_count in sorted_subnets:
        print(f'{subnet:>9}.*.* : {access_count}')
    print('-------------------------------------------')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        handle_error('Usage: python3 zadatak1.py <resource> <logfile>')

    resource = sys.argv[1]
    logfile = sys.argv[2]

    analyze_logfile(logfile, resource)
