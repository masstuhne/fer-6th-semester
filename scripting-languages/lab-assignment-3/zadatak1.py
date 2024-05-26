import sys


class Constants:
    EXIT_SUCCESS = 0,
    EXIT_FAILURE = 1


def handle_exit(exit_code, exit_message):
    print("Error message: " + exit_message)
    sys.exit(exit_code)


def parse_matrix(input_lines, index):
    first_line_info = input_lines[index].strip().split()
    num_of_rows = int(first_line_info[0])
    num_of_cols = int(first_line_info[1])

    index += 1
    return_matrix = {}

    while index < len(input_lines) and input_lines[index].strip() != '':

        if len(input_lines[index].strip().split()) != 3:
            handle_exit(Constants.EXIT_FAILURE, "Invalid input!")

        row, column, value = input_lines[index].strip().split()
        row = int(row)
        column = int(column)
        value = float(value)

        if row not in return_matrix:
            return_matrix[row] = {}

        return_matrix[row][column] = value
        index += 1

    return return_matrix, num_of_rows, num_of_cols, index


def print_matrix(matrix, num_of_rows, num_of_cols):
    full_matrix = [[0 for _ in range(num_of_cols)] for _ in range(num_of_rows)]

    for row in matrix:
        for col in matrix[row]:
            full_matrix[row][col] = matrix[row][col]
    for row in full_matrix:
        print('  ', end='')
        print('  '.join(f"{item:.2f}" for item in row))
    print()


def multiply_matrix(f_matrix, fm_row, fm_col, s_matrix, sm_row, sm_col):
    if fm_col != sm_row:
        handle_exit(Constants.EXIT_FAILURE, "Matrices cannot be multiplied!")

    result_matrix = {}
    for i in range(fm_row):
        for j in range(sm_col):
            temp_sum = 0
            for k in range(fm_col):
                temp_value_first = f_matrix[i].get(k, 0) if i in f_matrix else 0
                temp_value_second = second_matrix[k].get(j, 0) if k in s_matrix else 0
                temp_sum += temp_value_first * temp_value_second
            if temp_sum != 0:
                if i not in result_matrix:
                    result_matrix[i] = {}
                result_matrix[i][j] = temp_sum

    return result_matrix, fm_row, sm_col


def save_matrix(matrix, rows, columns, output_file):
    with open(output_file, 'w') as file:
        file.write(f"{rows} {columns}\n")
        for row in sorted(matrix.keys()):
            for col in sorted(matrix[row].keys()):
                file.write(f"{row} {col} {matrix[row][col]}\n")


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as file:
        input_lines = file.readlines()

    first_matrix, fm_row, fm_col, index = parse_matrix(input_lines, 0)
    second_matrix, sm_row, sm_col, _ = parse_matrix(input_lines, index + 1)

    print("first_matrix: ")
    print_matrix(first_matrix, fm_row, fm_col)
    print("second_matrix: ")
    print_matrix(second_matrix, sm_row, sm_col)

    result_matrix, rm_row, rm_col = multiply_matrix(first_matrix, fm_row, fm_col, second_matrix, sm_row, sm_col)

    print("first_matrix * second_matrix: ")
    print_matrix(result_matrix, rm_row, rm_col)

    save_matrix(result_matrix, rm_row, rm_col, output_file)
