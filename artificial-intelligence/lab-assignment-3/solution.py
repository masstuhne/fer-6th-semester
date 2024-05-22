import sys
import math


class TreeLeaf:
    def __init__(self, label_value):
        self.label = label_value

    def __str__(self):
        return f"TreeLeaf(label={self.label})"

    def __repr__(self):
        return f"TreeLeaf(label_value={repr(self.label)})"


class TreeNode:
    def __init__(self, feature, subtrees, dataset, depth):
        self.feature = feature
        self.subtrees = subtrees
        self.dataset = dataset
        self.depth = depth

    def __str__(self):
        return f"TreeNode(feature={self.feature}, subtrees={self.subtrees}, depth={self.depth})"

    def __repr__(self):
        return f"TreeNode(feature={repr(self.feature)}, subtrees={self.subtrees}, depth={self.depth})"


def predict_for_row(node, test_row):
    if isinstance(node, TreeLeaf):
        return node.label
    else:
        feature_index = features.index(node.feature)
        test_feature_value = test_row[feature_index]
        for subtree in node.subtrees:
            if subtree[0] == test_feature_value:
                return predict_for_row(subtree[1], test_row)

        # here goes the part for the unseen feature value (example: d is present as a feature value
        # and learn model doesn't know about it since it only saw a, b, c
        # it will get here since it won't pass if check in the for loop
        # we need to know the dataset from which the node was derived
        label_count_dict = {}
        label_column = len(node.dataset[0]) - 1
        for row in node.dataset:
            label_value = row[label_column]
            if label_value in label_count_dict:
                label_count_dict[label_value] += 1
            else:
                label_count_dict[label_value] = 1

        most_frequent_label = max(sorted(label_count_dict.keys()), key=lambda x: label_count_dict[x])
        return most_frequent_label


def calculate_entropy(data):
    label_column = len(data[0]) - 1
    unique_labels = {}
    for row in data:
        label_value = row[label_column]
        if label_value in unique_labels:
            unique_labels[label_value] += 1
        else:
            unique_labels[label_value] = 1

    entropy = 0
    data_number_of_rows = len(data)
    for key in unique_labels:
        temp_fraction = unique_labels[key] / data_number_of_rows
        entropy += (temp_fraction * math.log(temp_fraction, 2))
    entropy *= -1
    return entropy


def get_unique_feature_values(data, feature):
    feature_values = []
    for row in data:
        temp_feature_value = row[feature]
        if temp_feature_value not in feature_values:
            feature_values.append(temp_feature_value)
    return feature_values


def get_unique_label_values(data):
    label_column = len(data[0]) - 1
    label_values = []
    for row in data:
        temp_label_value = row[label_column]
        if temp_label_value not in label_values:
            label_values.append(temp_label_value)
    return label_values


def calculate_information_gain(data, feature, label_column):
    label_column = len(data[0]) - 1
    entropy_by_feature_value = {}
    number_by_feature_value = {}

    feature_values = get_unique_feature_values(data, feature)
    for value in feature_values:
        temp_data_with_value = []
        for row in data:
            # preventing false positives (in case multiple features have the same values) by not using value in row
            if row[feature].__eq__(value):
                temp_data_with_value.append(row)
        number_by_feature_value[value] = len(temp_data_with_value)
        entropy_by_feature_value[value] = calculate_entropy(temp_data_with_value)
        # dealing with negative zero
        if entropy_by_feature_value[value] == 0.0:
            entropy_by_feature_value[value] = 0.0

    information_gain = current_data_entropy
    for key in entropy_by_feature_value:
        temp_fraction = number_by_feature_value[key] / current_data_row_number
        information_gain -= (temp_fraction * entropy_by_feature_value[key])
    return information_gain


def calculate_most_frequent_label(data):
    label_column = len(data[0]) - 1
    most_frequent_label: str
    dict_label_count = {}
    for row in data:
        label_value = row[label_column]
        if label_value in dict_label_count:
            dict_label_count[label_value] += 1
        else:
            dict_label_count[label_value] = 1

    most_frequent_label = max(sorted(dict_label_count.keys()), key=lambda x: dict_label_count[x])
    return most_frequent_label, dict_label_count[most_frequent_label]


def handle_id3(data, data_parent, features):
    global current_data_entropy, current_depth
    if is_limited:
        if current_depth == limited_depth:
            return TreeLeaf(calculate_most_frequent_label(data)[0])
    if len(data) == 0:
        value = calculate_most_frequent_label(data_parent)
        return TreeLeaf(value)

    current_most_frequent_label, count = calculate_most_frequent_label(data)
    if len(features) == 0 or count == len(data):
        return TreeLeaf(current_most_frequent_label)

    information_gain_for_features = {}
    for feature_index in range(len(features)):
        temp_information_gain = calculate_information_gain(data, feature_index, current_label_column)
        information_gain_for_features[feature_index] = temp_information_gain

    max_gain_feature_index = max(information_gain_for_features, key=information_gain_for_features.get)
    max_gain_feature = features[max_gain_feature_index]
    features = features[:max_gain_feature_index] + features[max_gain_feature_index + 1:]

    subtrees = []
    values = get_unique_feature_values(data, max_gain_feature_index)
    current_depth += 1
    for value in values:
        new_data = []
        for row in data:
            if row[max_gain_feature_index].__eq__(value):
                temp_row = row[:max_gain_feature_index] + row[max_gain_feature_index + 1:]
                new_data.append(temp_row)
        current_data_entropy = calculate_entropy(data)
        t = handle_id3(new_data, data, features)
        subtrees.append((value, t))
    current_depth -= 1
    return TreeNode(max_gain_feature, subtrees, data, current_depth)


def handle_prediction(start_node, test_data):
    global real_and_predicted_labels
    label_column = len(test_data[0]) - 1
    test_data_size = len(test_data)
    number_of_correct_predictions = 0
    for row in test_data:
        prediction = predict_for_row(start_node, row)
        temp_tuple = (row[label_column], prediction)
        real_and_predicted_labels.append(temp_tuple)
        if prediction == row[label_column]:
            number_of_correct_predictions += 1
        print(prediction, end=" ")
    print()
    prediction_accuracy = number_of_correct_predictions / test_data_size
    return prediction_accuracy


def clear_temp_dict(temp_dict):
    for key in temp_dict.keys():
        temp_dict[key] = 0


def handle_confusion_matrix(test_data):
    label_values = sorted(get_unique_label_values(test_data))
    temp_dict = {}
    for label in label_values:
        temp_dict[label] = 0

    for label in label_values:
        clear_temp_dict(temp_dict)
        for label_tuple in real_and_predicted_labels:
            if label_tuple[0] == label:
                temp_dict[label_tuple[1]] += 1
        temp_dict = {key: temp_dict[key] for key in sorted(temp_dict)}
        values_list = list(temp_dict.values())
        for i, value in enumerate(values_list):
            if i == len(values_list) - 1:
                print(value, end="")
            else:
                print(value, end=" ")
        print()


def parse_input(path_to_file):
    return_data = []
    input_lines = open(path_to_file, 'r', encoding='utf-8').readlines()
    for line in input_lines:
        return_data.append(line.strip().split(","))
    return return_data


def parse_output(node, depth, prefix_print):
    if isinstance(node, TreeLeaf):
        print(f"{node.label}")
        return
    else:
        given_for = prefix_print
        first_time = True
        for subtree in node.subtrees:
            prefix_print = given_for + f"{depth}:{node.feature}={subtree[0]} "
            if first_time:
                first_time = False
                print(f"{depth}:{node.feature}={subtree[0]} ", end="")
            else:
                print(prefix_print, end="")
            parse_output(subtree[1], depth + 1, prefix_print)


# -------------------------------------------------------------------
# init part of the program

path_to_file_learn = ""
path_to_file_test = ""
is_limited = False
limited_depth: int

input_data = []
features = []
learn_data = []
test_data = []

current_depth = 0

# used for test
real_and_predicted_labels = []

# used both for learn and test
current_data_row_number: int
current_label_column: int
largest_feature_column: int
current_data_entropy = 0
learning_dictionary = {}

# -------------------------------------------------------------------

if __name__ == '__main__':
    path_to_file_learn = sys.argv[1]
    path_to_file_test = sys.argv[2]

    if len(sys.argv) > 3:
        is_limited = True
        limited_depth = int(sys.argv[3])

    # parsing learning data
    input_data = parse_input(path_to_file_learn)
    current_data_row_number = len(input_data) - 1
    current_label_column = len(input_data[0]) - 1
    largest_feature_column = current_label_column - 1

    features = input_data[0][:-1]
    learn_data = input_data[1:]

    current_data_entropy = calculate_entropy(learn_data)
    start_node = handle_id3(learn_data, learn_data, features)
    print("[BRANCHES]:")
    parse_output(start_node, 1, "")

    # parsing testing data
    input_data = parse_input(path_to_file_test)
    test_data = input_data[1:]

    print("[PREDICTIONS]: ", end="")
    accuracy = round(handle_prediction(start_node, test_data), 5)

    print(f"[ACCURACY]: {accuracy:.5f}")

    print("[CONFUSION_MATRIX]:")
    handle_confusion_matrix(test_data)
