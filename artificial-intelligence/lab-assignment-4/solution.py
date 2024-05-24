import sys
import math
import numpy as np


class NeuralNetwork:
    def __init__(self, architecture):
        self.architecture = architecture
        self.weights = []
        self.biases = []
        self.num_of_layers = 0
        self.mean_squared_error = 0
        self.fitness = 0
        self.initialize_weights()

    def initialize_weights(self):
        layers = [input_data_dimension]
        for size in self.architecture.split('s'):
            if size != '':
                layers.append(int(size))
        layers.append(output_data_dimension)
        for i in range(1, len(layers)):
            weight_matrix = np.random.normal(0, 0.01, (layers[i], layers[i - 1]))
            bias_vector = np.random.normal(0, 0.01, (layers[i], 1))
            self.weights.append(weight_matrix)
            self.biases.append(bias_vector)
        self.num_of_layers = len(layers)

    def apply_sigmoid(self, result):
        return 1 / (1 + np.exp(-result))

    def forward_pass(self, data):
        sum_of_squared_errors = 0

        for i in range(len(data)):
            curr_row = data[i]
            y = float(curr_row[-1])
            x = np.asarray(curr_row[:-1], dtype=np.float64).reshape(-1, 1)
            # x = x.reshape(1, -1)

            curr_layer = 0
            for weight in self.weights:
                # print("W: ", weight)
                # print("X: ", x)
                # print(x.shape)
                matrix_multiple = np.dot(weight, x)
                # print("Matrix multiplication: ", matrix_multiple)
                # print("BIAS: ", self.biases[curr_layer])
                result = np.add(matrix_multiple, self.biases[curr_layer])
                # print("R: ", result)
                curr_layer += 1

                if curr_layer < (self.num_of_layers - 1):
                    result = self.apply_sigmoid(result)
                else:
                    result = result.item()
                    sum_of_squared_errors += math.pow(y - result, 2)

                x = result
        return sum_of_squared_errors

    def compute_mean_squared_error(self, data):
        sum_of_squared_errors = self.forward_pass(data)
        mse = sum_of_squared_errors / len(data)
        self.mean_squared_error = mse
        self.fitness = 1 / self.mean_squared_error


def load_input_args():
    args = {}
    for i in range(1, len(sys.argv), 2):
        key = sys.argv[i].lstrip('--').strip()
        value = sys.argv[i + 1].strip()
        args[key] = value
    return args


def parse_input(path_to_file):
    return_data = []
    input_lines = open(path_to_file, 'r', encoding='utf-8').readlines()
    for line in input_lines:
        return_data.append(line.strip().split(","))
    return return_data


def generate_start_population(pop_size, nn_architecture):
    population = []
    for i in range(pop_size):
        population.append(NeuralNetwork(nn_architecture))
    return population


def select_parents(population, population_fitness):
    population_fitness_sum = sum(population_fitness)
    population_probabilities = [fitness / population_fitness_sum for fitness in population_fitness]
    parent1 = np.random.choice(population, p=population_probabilities)
    parent2 = np.random.choice(population, p=population_probabilities)
    return parent1, parent2


def handle_crossover(parent1, parent2):
    child1, child2 = NeuralNetwork(nn_architecture), NeuralNetwork(nn_architecture)
    for i in range(len(parent1.weights)):
        child1.weights[i] = (parent1.weights[i] + parent2.weights[i]) / 2
        child1.biases[i] = (parent1.biases[i] + parent2.biases[i]) / 2
        child2.weights[i] = (parent1.weights[i] + parent2.weights[i]) / 2
        child2.biases[i] = (parent1.biases[i] + parent2.biases[i]) / 2
    return child1, child2


def handle_mutate(neural_network):
    for weight in neural_network.weights:
        given_random = np.random.random()
        if given_random < p:
            weight += np.random.normal(loc=0, scale=K, size=weight.shape)

    for bias in neural_network.biases:
        given_random = np.random.random()
        if given_random < p:
            bias += np.random.normal(loc=0, scale=K, size=bias.shape)


def run_genetic_algorithm(population, iterations):
    stop = False
    curr_iteration = 0

    curr_population = population
    best_neural_network = None

    while not stop:
        curr_iteration += 1
        for nn in curr_population:
            nn.compute_mean_squared_error(train_data)

        sorted_population = sorted(
            curr_population,
            key=lambda neural_network: neural_network.mean_squared_error
        )

        elite_population = sorted_population[:elitism]

        if curr_iteration % 2000 == 0:
            best_elite = elite_population[0].mean_squared_error
            print(f'[Train error @{curr_iteration}]: {best_elite:.6f}')
            if curr_iteration == iterations:
                stop = True
                best_neural_network = elite_population[0]
                break

        new_population = []
        population_fitness_list = [nn.fitness for nn in elite_population]
        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(elite_population, population_fitness_list)
            child1, child2 = handle_crossover(parent1, parent2)
            handle_mutate(child1)
            handle_mutate(child2)
            new_population.append(child1)
            if len(new_population) == pop_size:
                break
            new_population.append(child2)

        curr_population = new_population.copy()

    return best_neural_network

# -------------------------------------------------------------------
# init part of the program

input_data_dimension: int
output_data_dimension = 1

target_col_train: int
target_col_test: int

# consists of several 'neural networks'/individuals/chromosomes that can possibly
# solve a problem
population = []

# -------------------------------------------------------------------


if __name__ == '__main__':
    args = load_input_args()

    train_data = parse_input(args['train'])
    test_data = parse_input(args['test'])

    train_data = train_data[1:]
    test_data = test_data[1:]

    input_data_dimension = len(train_data[0]) - 1

    target_col_train = len(train_data[0]) - 1
    target_col_test = len(test_data[0]) - 1

    pop_size = int(args['popsize'])
    elitism = int(args['elitism'])
    p = float(args['p'])
    K = float(args['K'])
    iterations = int(args['iter'])
    nn_architecture = args['nn']

    population = generate_start_population(pop_size, nn_architecture)

    best_neural_network = run_genetic_algorithm(population, iterations)
    best_neural_network.compute_mean_squared_error(test_data)
    print(f'[Test error]: {best_neural_network.mean_squared_error:.6f}')
