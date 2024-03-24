import sys


class Node:
    def __init__(self, state_name, parent, curr_total_value: float):
        self.state_name = state_name
        self.parent = parent
        self.curr_total_value = curr_total_value


def print_result(found_solution, algorithm, num_of_visited_states, path_to_solution, total_cost):
    if found_solution:
        print('# ' + algorithm + ' ' + path_to_file)
        print('[FOUND_SOLUTION]: yes')
        print("[STATES_VISITED]: " + str(num_of_visited_states))
        print("[PATH_LENGTH]: " + str(len(path_to_solution)))
        print("[TOTAL_COST]: " + str(total_cost))
        print("[PATH]: " + ' => '.join(path_to_solution))
    else:
        print('[FOUND_SOLUTION]: no')


def parse_input():
    global start_state, goal_states, transitions
    i = 0
    for line in input_lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        else:
            i += 1
            if i == 1:
                start_state = line
            elif i == 2:
                goal_states = line.split(' ')
            else:
                state, state_leads_to = line.split(':')
                state = state.strip()
                if state_leads_to.__eq__(''):
                    transitions[state] = None
                else:
                    state_leads_to = state_leads_to.strip()
                    transitions[state] = sorted(state_leads_to.split(' '))


def run_bfs():
    parse_input()
    # open_states will behave like a queue
    open_states = []
    # closed_states will behave like a set
    closed_states = set()

    found_solution = False
    # path_to_solution will behave like a stack
    path_to_solution = []
    total_cost = 0

    open_states.append(Node(state_name=start_state,
                            parent=None,
                            curr_total_value=0))

    # while !isEmpty(open_states)
    while open_states:
        head = open_states.pop(0)
        head_state_name = head.state_name
        closed_states.add(head_state_name)

        if head_state_name in goal_states:
            found_solution = True
            total_cost = head.curr_total_value

            while head:
                path_to_solution.append(head.state_name)
                head = head.parent
            break

        next_states = transitions[head_state_name]
        if next_states is not None:
            for next_state in next_states:
                next_state_name, next_state_cost = next_state.split(',')
                if next_state_name not in closed_states:
                    open_states.append(Node(state_name=next_state_name,
                                            parent=head,
                                            curr_total_value=head.curr_total_value + float(next_state_cost)))

    if found_solution:
        print_result(True, 'BFS', len(closed_states), path_to_solution, total_cost)
    else:
        print_result(False, 'BFS', len(closed_states), path_to_solution, total_cost)
    return


def run_ucs():
    return


def run_a_star():
    return


# -------------------------------------------------------------------
# init part of the program

algorithm_in_use = ''

index_ss = sys.argv.index('--ss')
path_to_file = sys.argv[index_ss + 1]

input_lines = open(path_to_file, 'r', encoding='utf-8').readlines()

start_state = ''
goal_states = []
transitions = {}

# -------------------------------------------------------------------

if __name__ == '__main__':
    if sys.argv.__contains__('--alg'):
        index = sys.argv.index('--alg')
        algorithm_in_use = sys.argv[index + 1]

        if algorithm_in_use == 'bfs':
            run_bfs()
        elif algorithm_in_use == 'ucs':
            run_ucs()
        else:
            run_a_star()
