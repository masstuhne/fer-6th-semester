import sys


class Constants:
    EXIT_SUCCESS = 0,
    EXIT_FAILURE = 1


def handle_exit(exit_code, exit_message):
    print("Error message: " + exit_message)
    sys.exit(exit_code)


def calculate_hd_value(values, q):
    values = sorted(values)
    index = int(len(values) * q)
    return values[index]


def process_file(given_file):
    with open(given_file, 'r') as file:
        input_lines = file.readlines()

    parsed_lines = []
    for line in input_lines:
        parsed_lines.append(list(map(float, line.split())))

    print("Hyp#Q10#Q20#Q30#Q40#Q50#Q60#Q70#Q80#Q90")
    for i, line in enumerate(parsed_lines):
        line = sorted(line)

        q_values = []
        for j in range(1, 10):
            q_values.append(line[int(len(line) * (j/10)) - 1])

        print(f"{i + 1:03d}#{'#'.join(map(str, q_values))}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        handle_exit(Constants.EXIT_FAILURE, "Invalid number of arguments")

    input_file = sys.argv[1]
    process_file(input_file)
