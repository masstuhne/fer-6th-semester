import os
import sys


class Constants:
    EXIT_SUCCESS = 0,
    EXIT_FAILURE = 1


def handle_exit(exit_code, exit_message):
    print("Error message: " + exit_message)
    sys.exit(exit_code)


def parse_students(students_file):
    students = {}
    grades = {}
    labs = {}
    with open(students_file, "r") as file:
        for line in file:
            line_parts = line.strip().split()
            jmbag = line_parts[0]
            surname = line_parts[1]
            name = line_parts[2]
            students[jmbag] = f"{surname}, {name}"
            grades[jmbag] = {}
            labs[jmbag] = set()
    return students, grades, labs


if __name__ == '__main__':
    if len(sys.argv) != 2:
        handle_exit(Constants.EXIT_FAILURE, "Invalid number of arguments!")

    directory = sys.argv[1]

    students_file = os.path.join(directory, 'studenti.txt')
    if not os.path.exists(students_file):
        handle_exit(Constants.EXIT_FAILURE, "Students.txt does not exist in the given directory!")

    students, grades, labs = parse_students(students_file)

    all_labs = []

    for file in os.listdir(directory):
        if file.startswith('Lab'):
            filename_parts = file.split('_')
            num_of_lab = int(filename_parts[1])
            if num_of_lab not in all_labs:
                all_labs.append(num_of_lab)

            with open(os.path.join(directory, file), 'r') as f:
                for line in f:
                    jmbag, grade = line.strip().split()
                    if num_of_lab in labs[jmbag]:
                        print("Warning: student with JMBAG: " + str(jmbag) + " was already graded in lab " + str(num_of_lab) + "!")
                    else:
                        labs[jmbag].add(num_of_lab)
                        grades[jmbag][num_of_lab] = grade

    print("{:<12} {:<20} {}".format("JMBAG", "Prezime, Ime", '   '.join(f"L{i + 1}" for i in range(len(all_labs)))))
    for jmbag, fullName in students.items():
        print(f"{jmbag:<12} {fullName:<20}", end='')
        for lab in sorted(all_labs):
            if lab not in grades[jmbag].keys():
                print(" -   ", end='')
            else:
                print(f" {float(grades[jmbag][lab]):3.1f} ", end='')
        print()
