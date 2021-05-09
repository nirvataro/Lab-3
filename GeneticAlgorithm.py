import random
import time
import numpy as np
from psutil import cpu_freq
from MetaHeuristicFramework import VRP


############## constants ###############
GA_POPSIZE = 1000        # ga population size
GA_ELITRATE = .2		    # elitism rate
GA_MUTATIONRATE = .25      # mutation rate
########################################


class Gen:
    def __init__(self, graph, age=0):
        self.graph = graph.__deepcopy__()
        self.fitness = 0
        self.age = age

    def calculate_fitness(self):
        return 0

    def arrange_nodes(self):
        pass

    def mutate(self):
        random_node = random.choice(self.graph.nodes[1:])
        random_color = random.choice([i for i in range(self.graph.k) if i != random_node.color])
        self.color_node(random_node, random_color)
        self.fitness = self.calculate_fitness()

class GeneticAlgorithm:
    def __init__(self, graph, popsize=GA_POPSIZE, elite_rate=GA_ELITRATE, mutation_rate=GA_MUTATIONRATE):
        self.empty_graph = graph
        self.pop_size = popsize
        self.elite_size = round(elite_rate*popsize)
        self.mutation_rate = mutation_rate
        self.gen_arr, self.buffer = self.init_population()

    def init_population(self):
        gen_arr = [self.random_coloring() for _ in range(self.pop_size)]
        buffer = [None for _ in range(self.pop_size)]
        return gen_arr, buffer

    def random_coloring(self):
        new_graph = self.empty_graph.__deepcopy__()
        for node in new_graph.nodes:
            random_color = random.choice(list(range(new_graph.k)))
            new_graph.color_node(node, random_color)
        age = random.randint(0, 4)
        gen = Gen(new_graph, age=age)
        gen.arrange_nodes()
        gen.calculate_fitness()
        return gen

    # sorts population by key fitness value
    def sort_by_fitness(self):
        self.gen_arr.sort(key=lambda x: x.fitness)

    # takes GA_ELITRATE percent to next generation
    def elitism(self):
        for i in range(self.elite_size):
            self.buffer[i] = self.gen_arr[i].__deepcopy__()

    def crossover(self, gen1, gen2):
        newgen = Gen(self.empty_graph)
        for node_number in range(self.empty_graph.V):
            color1 = gen1.graph.nodes[node_number].color
            color2 = gen2.graph.nodes[node_number].color
            color = random.choice([color1, color2])
            newgen.color_node(node_number, color)
        newgen.arrange_nodes()
        newgen.calculate_fitness()
        return newgen

    # RWS selection
    def selection(self):
        # sel will store selected parents to mate
        total_fitness = sum([gen.fitness for gen in self.gen_arr])

        # randomize a number between 0-sum of all fitness, find where that gen is and use as parent
        ran_selection = random.uniform(0, total_fitness)
        current, j = 0, 0
        while current < ran_selection:
            current += self.gen_arr[j].fitness
            j += 1
        parent1 = self.gen_arr[j]
        # randomize a number between 0-sum of all fitness, find where that gen is and use as parent
        ran_selection = random.uniform(0, total_fitness)
        current, j = 0, 0
        while current < ran_selection:
            current += self.gen_arr[j].fitness
            j += 1
        parent2 = self.gen_arr[j]
        return parent1, parent2

    def mate(self):
        self.elitism() # filling buffer with best of this generation
        for gen in self.gen_arr:
            gen.age += 1

        can_mate = self.can_mate()

        # mating parents
        for i in range(self.elite_size, self.pop_size):
            p1, p2 = self.selection()
            self.buffer[i] = self.crossover(p1, p2)

            # in GA_MUTATIONRATE chance new child will mutate
            if random.random() <= self.mutation_rate:
                self.buffer[i].mutate()
        self.buffer, self.gen_arr = self.gen_arr, self.buffer

class REGULAR:
    def selection(self, gen_arr, k):
        return [gen_arr[random.randint(0, int(GA_POPSIZE/2))] for i in range(k)]


# Part 2 - Ex.2 creating array of possible parents by age
def ageing(gen_arr, min_age):
    can_mate = []
    for g in gen_arr:
        if g.age >= min_age:
            can_mate.append(g)
    return can_mate


# age updater for every iteration
def birthday(gen_arr):
    for g in gen_arr:
        g.age += 1
    return gen_arr


##################################################################################################


# generic mating function
# supports elitism, aging, selection types, crossovers, possible string values, different target lengths



# calculates average fitness of current generation
def avg_fit(gen_arr):
    fit_arr = [g.cost[0] for g in gen_arr]
    return np.mean(fit_arr)


# calculates STD of current generation
def std_fit(gen_arr):
    fit_arr = [g.cost[0] for g in gen_arr]
    return np.std(fit_arr)


# print function
def print_best(gen_arr, timer):
    print("Genetic Algorithm: ")
    print(gen_arr[0])
    print("Avg fitness of gen: {}".format(avg_fit(gen_arr)))
    print("Fitness STD: {}".format(std_fit(gen_arr)))
    iter_time = time.time() - timer
    print("Total time of generation: {}".format(iter_time))
    print("Total clock ticks (CPU)) of generation: {}\n".format(iter_time*cpu_freq()[0]*(2**20)))


crossover_dictionary = {0: OXCrossover(), 1: PMXCrossover()}
selection_dictionary = {0: RWS(), 1: SUS(), 2: TOURNAMENT(), 3: REGULAR()}
mutation_dictionary = {0: SwapMutation(), 1: ScrambleMutation()}


def gen_alg(cross_type, select_type, mutate_type, capacity, dist_matrix, goods, search_time=120):
    gen_arr, buffer = init_population(capacity, dist_matrix, goods)
    cross = crossover_dictionary[cross_type]
    select = selection_dictionary[select_type]
    mut = mutation_dictionary[mutate_type]
    end_time = time.time() + search_time
    time_left = end_time - time.time()
    total_timer = time.time()
    best = np.inf
    i = 0
    while time_left > 0:
        gen_timer = time.time()

        gen_arr = sort_by_fitness(gen_arr)
        if gen_arr[0].cost[0] < best:
            print_best(gen_arr, gen_timer)
            best = gen_arr[0].cost[0]
        if gen_arr[0].cost[0] == 0:
            break

        gen_arr = birthday(gen_arr)
        # mate and swap between buffer and gen_arr
        buffer, gen_arr = mate(gen_arr, buffer, cross, select, mut, capacity, dist_matrix, goods)
        time_left = end_time - time.time()
        i += 1
    total_time = time.time() - total_timer
    print("Total time : {}\nTotal clock ticks : {}\nTotal iterations:{}".format(total_time, total_time*cpu_freq()[0]*2**20, i+1))
    return gen_arr[0].cost[0], progress
