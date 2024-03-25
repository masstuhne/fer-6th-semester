import sys
from heapq import heappush, heappop


class Node:
    def __init__(self, state_name, parent, curr_total_value: float, used_in_a_star: bool):
        self.state_name = state_name
        self.parent = parent
        self.curr_total_value = curr_total_value
        self.used_in_a_star = used_in_a_star
        self.heuristic_value = float(heuristics[state_name]) if used_in_a_star else None

    def __lt__(self, other):
        if not self.used_in_a_star:
            if self.curr_total_value < other.curr_total_value:
                return True
            elif self.curr_total_value == other.curr_total_value:
                return self.state_name < other.state_name
            else:
                return False
        else:
            self_total = self.heuristic_value + self.curr_total_value
            other_total = other.heuristic_value + other.curr_total_value
            if self_total < other_total:
                return True
            elif self_total == other_total:
                return self.state_name < other.state_name
            else:
                return False


def print_result(found_solution, algorithm, num_of_visited_states, path_to_solution, total_cost):
    if found_solution:
        print('# ' + algorithm + ' ' + path_to_file)
        print('[FOUND_SOLUTION]: yes')
        print("[STATES_VISITED]: " + str(num_of_visited_states))
        print("[PATH_LENGTH]: " + str(len(path_to_solution)))
        print("[TOTAL_COST]: " + str(total_cost))
        print("[PATH]: " + ' => '.join(path_to_solution.reverse()))
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


def parse_input_heuristics():
    global heuristics
    index_h = sys.argv.index('--h')
    path_to_file_heuristics = sys.argv[index_h + 1]

    input_lines_heuristics = sorted(open(path_to_file_heuristics, 'r', encoding='utf-8').readlines())

    for line in input_lines_heuristics:
        line = line.strip()
        if line.startswith('#'):
            continue
        else:
            state, heuristic_value = line.split(':')
            state = state.strip()
            heuristic_value = heuristic_value.strip()
            heuristics[state] = float(heuristic_value)


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
                            curr_total_value=0,
                            used_in_a_star=False))

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
                                            curr_total_value=head.curr_total_value + float(next_state_cost),
                                            used_in_a_star=False))

    if found_solution:
        print_result(True, 'BFS', len(closed_states), path_to_solution, total_cost)
    else:
        print_result(False, 'BFS', len(closed_states), path_to_solution, total_cost)
    return


def run_ucs():
    parse_input()
    # open_states will behave like a heap queue / priority queue
    open_states = []
    # closed_states will behave like a set
    closed_states = set()

    found_solution = False
    # path_to_solution will behave like a stack
    path_to_solution = []
    total_cost = 0

    heappush(open_states, Node(state_name=start_state,
                               parent=None,
                               curr_total_value=0,
                               used_in_a_star=False))

    # while !isEmpty(open_states)
    while open_states:
        head = heappop(open_states)
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
                    heappush(open_states, Node(state_name=next_state_name,
                                               parent=head,
                                               curr_total_value=head.curr_total_value + float(next_state_cost),
                                               used_in_a_star=False))

    if found_solution:
        print_result(True, 'UCS', len(closed_states), path_to_solution, total_cost)
    else:
        print_result(False, 'UCS', len(closed_states), path_to_solution, total_cost)
    return


def run_a_star():
    parse_input()
    parse_input_heuristics()
    # open_states will behave like a heap queue / priority queue
    open_states = []
    # closed_states will behave like a set
    closed_states = set()

    found_solution = False
    # path_to_solution will behave like a stack
    path_to_solution = []
    total_cost = 0

    heappush(open_states, Node(state_name=start_state,
                               parent=None,
                               curr_total_value=0,
                               used_in_a_star=True))

    # while !isEmpty(open_states)
    while open_states:
        head = heappop(open_states)
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
                    heappush(open_states, Node(state_name=next_state_name,
                                               parent=head,
                                               curr_total_value=head.curr_total_value + float(next_state_cost),
                                               used_in_a_star=True))

    if found_solution:
        print_result(True, 'A-STAR', len(closed_states), path_to_solution, total_cost)
    else:
        print_result(False, 'A-STAR', len(closed_states), path_to_solution, total_cost)
    return

def run_admissibility_check():
    parse_input()
    parse_input_heuristics()

    is_admissible = True

    

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
heuristics = {}

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
    elif sys.argv.__contains__('--check-optimistic'):
        run_admissibility_check()
    elif sys.argv.__contains__('--check-consistent'):
        None
