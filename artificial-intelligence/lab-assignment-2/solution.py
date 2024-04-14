import sys
from heapq import heappush, heappop


class Clause:
    def __init__(self, literals, number, from_1=None, from_2=None):
        self.literals = literals
        self.number = number
        self.from_1 = from_1
        self.from_2 = from_2

    def __eq__(self, other):
        return isinstance(other, Clause) and \
            self.literals == other.literals

    def __hash__(self):
        return hash(self.literals)

    def __repr__(self):
        return "({}, {})".format(self.number, self.literals)

    def __lt__(self, other):
        if self.number < other.number:
            return True

    def copy(self):
        return Clause(self.literals.copy(), self.number, self.from_1, self.from_2)


def parse_input():
    global goal_clause, current_index

    for index, line in enumerate(input_lines):
        line = line.strip().lower()
        if line.startswith('#'):
            continue
        else:
            current_index += 1

            if line.__contains__(' v '):
                literals = line.split(' v ')

                literals_set = frozenset(literal.strip() for literal in literals)

                if index == (len(input_lines) - 1):
                    goal_clause = Clause(literals_set, current_index)
                else:
                    starting_clauses_set.add(Clause(literals_set, current_index))
            else:
                literals_set = frozenset([line])

                if index == (len(input_lines) - 1):
                    goal_clause = Clause(literals_set, current_index)
                else:
                    starting_clauses_set.add(Clause(literals_set, current_index))


def handle_success_output():
    global nil_clause, index_of_last_starter_clause, starting_clauses_set

    collected_clauses_for_output = []
    collected_parents = []
    collected_clauses = [nil_clause]

    while not len(collected_clauses) == 0:
        for clause in collected_clauses:
            if (not (clause.from_1 is None)) and (not (clause.from_2 is None)):
                if clause not in collected_clauses_for_output:
                    heappush(collected_clauses_for_output, clause)
                    if (clause.from_1.number <= index_of_last_starter_clause) and (clause.from_2.number <= index_of_last_starter_clause):
                        pass
                    else:
                        collected_parents.append(clause.from_1)
                        collected_parents.append(clause.from_2)
        collected_clauses = collected_parents
        collected_parents = []

    start_clauses_for_output = []

    if cooking_mode:
        starting_clauses_set = starting_clauses_set_copy

    for clause in starting_clauses_set:
        heappush(start_clauses_for_output, clause)
    for clause in negated_goal_clauses:
        heappush(start_clauses_for_output, clause)

    while start_clauses_for_output:
        clause = heappop(start_clauses_for_output)
        string_set = {str(literal) for literal in clause.literals}
        print(str(clause.number) + '.' + ' ' + ' v '.join(string_set))
    print('===============')
    while collected_clauses_for_output:
        clause = heappop(collected_clauses_for_output)
        string_set = {str(literal) for literal in clause.literals}
        parent_1_number = clause.from_1.number
        parent_2_number = clause.from_2.number
        print(str(clause.number) + '.' + ' ' + ' v '.join(string_set) + ' ( ' + str(parent_1_number) + ', ' + str(
            parent_2_number) + ' )')
    print('===============')
    string_set = {str(literal) for literal in goal_clause.literals}
    print('[CONCLUSION]: ' + ' v '.join(string_set) + ' is true')


def handle_failure_output():
    string_set = {str(literal) for literal in goal_clause.literals}
    print('[CONCLUSION]: ' + ' v '.join(string_set) + ' is unknown')


def negate_literal(literal):
    if literal.__contains__('~'):
        return literal[1:]
    else:
        return "~" + literal


def resolve_redundancy(clauses):
    redundant_clauses = set()

    for c1 in clauses:
        for c2 in clauses:
            if not c1.__eq__(c2):
                l1 = c1.literals
                l2 = c2.literals
                if l1.issubset(l2):
                    redundant_clauses.add(c2)
    clauses.difference_update(redundant_clauses)


def resolve_tautology(clauses):
    for_removal_clauses = set()

    for clause in clauses:
        for literal in clause.literals:
            if (literal in clause.literals) and (negate_literal(literal) in clause.literals):
                for_removal_clauses.add(clause)
                break
    clauses.difference_update(for_removal_clauses)


def get_clauses_from_negated_goal_state(goal_clause):
    global current_index
    negated_goal_clauses = set()
    # because the goal state ("clause") did ++1 in parseInput and now we don't need it (the goal state)
    current_index -= 1

    for literal in goal_clause.literals:
        # frozenset expects an iterable
        # so with passing only ~X it iterates through it
        temp_frozen_set = frozenset([negate_literal(literal)])
        current_index += 1
        negated_goal_clauses.add(Clause(temp_frozen_set, current_index))
    return negated_goal_clauses


def resolve_new_clauses(clause1, clause2):
    global current_index, nil_clause
    new_clauses = set()
    nil_found = False

    for clause1_literal in clause1.literals:
        for clause2_literal in clause2.literals:
            # why do we not care if the literals are the same:
            # we can only resolve clauses that have complementary literals
            # we then resolve them
            # this will give us a new clause
            # , or it will cancel out to an empty clause which means that we successfully proved
            # that resolution procedure derived NIL, hence premises (start + negated goal)
            # (clauses - premises in a form of disjunction of literals) are inconsistent,
            # hence we proved that the goal premise is a logical consequence of the starting ones
            if clause1_literal.__eq__(negate_literal(clause2_literal)):
                temp_clause_set = set(clause1.literals.union(clause2.literals))
                temp_clause_set.discard(clause1_literal)
                temp_clause_set.discard(clause2_literal)
                if len(temp_clause_set) == 0:
                    current_index += 1
                    new_clauses.add(Clause(frozenset(['NIL']), current_index, clause1, clause2))
                    nil_clause = Clause(frozenset(['NIL']), current_index, clause1, clause2)
                    nil_found = True
                    return new_clauses, nil_found
                else:
                    current_index += 1
                    new_clauses.add(Clause(frozenset(temp_clause_set), current_index, clause1, clause2))
    return new_clauses, nil_found


def handle_cooking():
    global sos_clauses, starting_clauses_set_copy, current_index, index_of_last_starter_clause, negated_goal_clauses, goal_clause
    for index, line in enumerate(input_lines_actions):
        line = line.strip().lower()
        if line.startswith('#'):
            continue
        else:
            remember_current_index = current_index
            print()
            print('User command: ' + line)
            if line.__contains__('?'):
                current_index += 1
                line = line.strip(' ?')
                if line.__contains__(' v '):
                    print()
                    print('User command: ' + line)
                    literals = line.split(' v ')
                    literals_set = frozenset(literal.strip() for literal in literals)
                else:
                    literals_set = frozenset([line])

                goal_clause = Clause(literals_set, current_index)
                negated_goal_clauses = get_clauses_from_negated_goal_state(goal_clause)
                sos_clauses.update(negated_goal_clauses)

                index_of_last_starter_clause = current_index

                handle_resolution_check()

                sos_clauses.clear()
                current_index = remember_current_index
            elif line.__contains__('+'):
                current_index += 1
                line = line.strip(' +')
                if line.__contains__(' v '):
                    literals = line.split(' v ')
                    literals_set = frozenset(literal.strip() for literal in literals)
                else:
                    literals_set = frozenset([line])

                append_clause = Clause(literals_set, current_index)
                starting_clauses_set_copy.add(append_clause)
            elif line.__contains__('-'):
                line = line.strip(' -')
                if line.__contains__(' v '):
                    literals = line.split(' v ')
                    literals_set = frozenset(literal.strip() for literal in literals)
                else:
                    literals_set = frozenset([line])

                delete_clause = Clause(literals_set, None)
                starting_clauses_set_copy.remove(delete_clause)


def handle_resolution_check():
    global sos_clauses, current_index

    resolve_redundancy(starting_clauses_set_copy)
    resolve_tautology(starting_clauses_set_copy)

    help_clauses = starting_clauses_set_copy.copy()
    new_clauses = set()

    added_something_new = True
    while added_something_new:
        added_something_new = False

        for sos_clause in sos_clauses:
            for clause in help_clauses:
                resolvents, nil_found = resolve_new_clauses(sos_clause, clause)
                if nil_found:
                    handle_success_output()
                    return
                if len(resolvents) > 0:
                    if not resolvents.issubset(sos_clauses.union(help_clauses)):
                        added_something_new = True
                        new_clauses.update(resolvents)
            # in pseudocode on the presentation it says clauses = starting AND negated goal
            # so this puts the sos_clause in the help_clauses set so it can be paired with
            # other sos_clauses from the sos_clauses set --> this way we tried to resolve new
            # clauses from each combination of start AND negated goal, TLDR got what the presentation says
            help_clauses.add(sos_clause)
        resolve_tautology(help_clauses)
        resolve_redundancy(help_clauses)
        resolve_tautology(new_clauses)
        resolve_redundancy(new_clauses)

        # old sos_clauses are all added in the help_clauses so the relation: clauses = clauses union new from
        # the presentation holds this way; since we are again making combinations from new clauses and old ones
        # being sos_clauses + help_clauses
        sos_clauses = new_clauses
        new_clauses = set()

    handle_failure_output()


# -------------------------------------------------------------------
# init part of the program

path_to_file_clauses = sys.argv[2]
input_lines = open(path_to_file_clauses, 'r', encoding='utf-8').readlines()

path_to_file_actions = ''
input_lines_actions = None
cooking_mode = False

current_index = 0
index_of_last_starter_clause = 0

starting_clauses_set = set()
starting_clauses_set_copy = set()
sos_clauses = set()
negated_goal_clauses = None
# it should be called goal_state, but since this format is easier to parse, it is ok
# consider changing it
goal_clause = None
nil_clause = None
# -------------------------------------------------------------------


if sys.argv.__contains__('resolution'):
    parse_input()

    starting_clauses_set_copy = starting_clauses_set.copy()

    negated_goal_clauses = get_clauses_from_negated_goal_state(goal_clause)

    sos_clauses.update(negated_goal_clauses)

    index_of_last_starter_clause = current_index

    handle_resolution_check()
elif sys.argv.__contains__('cooking'):
    path_to_file_actions = sys.argv[3]
    input_lines_actions = open(path_to_file_actions, 'r', encoding='utf-8').readlines()

    parse_input()
    starting_clauses_set.add(goal_clause)

    starting_clauses_set_copy = starting_clauses_set.copy()

    cooking_mode = True
    handle_cooking()
