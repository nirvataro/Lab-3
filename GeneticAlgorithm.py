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


# class of genetic (GA_STRUCT in cpp example)
class Genetic(VRP):
    def __init__(self, capacity, dist_mat, goods, permutation):
        super().__init__(capacity, dist_mat, goods, config=permutation)
        self.age = random.randint(0, 4)


# PMX crossover from moodle
class PMXCrossover:
    def crossover(self, gen1, gen2):
        N = len(gen1.goods) - 1
        iter = random.randint(1, int(N/2))
        child = [i for i in gen1.config]

        # do PMX crossover a random number of times
        for it in range(iter):
            index = random.randint(0, N-1)
            val1 = gen1.config[index]
            val2 = gen2.config[index]
            for i in range(N):
                if child[i] == val1:
                    child[i] = val2
                elif child[i] == val2:
                    child[i] = val1
        return child


# OX crossover from moodle
class OXCrossover:
    def crossover(self, gen1, gen2):
        N = len(gen1.goods) - 1
        child = [i for i in gen1.config]
        # val1 will store half of the values randomly
        val1 = random.sample(range(1, N+1), N // 2)
        # val2 will store the remaining values
        val2 = [i for i in gen2.config if i not in val1]
        v2 = 0
        for i in range(len(child)):
            if child[i] not in val1:
                child[i] = val2[v2]
                v2 += 1
        return child


# for scaling the problem and creating a max instead min (for RWS, SUS) we used 1/sqrt(fitness scaling)
def scale(gen_arr):
    scaled_fit = [None for i in range(len(gen_arr))]
    for i in range(len(gen_arr)):
        scaled_fit[i] = 1/gen_arr[i].cost[0]**0.5
    return sum(scaled_fit), scaled_fit


# implementation of RWS selection type (uses scaling function above)
class RWS:
    def selection(self, gen_arr, parent=2):
        # sel will store selected parents to mate
        sel = [None for i in range(parent)]
        total_fitness, scaled_fit = scale(gen_arr)
        for i in range(parent):
            # randomize a number between 0-sum of all fitness, find where that gen is and use as parent
            ran_selection = random.uniform(0, total_fitness)
            current, j = 0, 0
            while current < ran_selection:
                current += scaled_fit[i]
                j += 1
            sel[i] = gen_arr[j]
        return sel


class SUS:
    def selection(self, gen_arr, parent=2):
        sel = [None for i in range(parent)]
        total_fitness, scaled_fit = scale(gen_arr)
        # randomize only once as written in algorithm
        # similar to implementation of RWS
        ran = random.uniform(0, total_fitness/GA_POPSIZE)
        delta = total_fitness/parent
        for i in range(parent):
            fitness = ran + i*delta
            current, j = 0, 0
            while current < fitness:
                current += gen_arr[j].cost[0]
                j += 1
            sel[i] = gen_arr[j]
        return sel


class TOURNAMENT:
    def selection(self, gen_arr, k_tour_size, parent=2):
        sel = [None for i in range(parent)]
        for i in range(parent):
            # selects k random parents and uses best of them fot mating
            tournament = random.choices(gen_arr, k=k_tour_size)
            sel[i] = min(tournament, key=lambda x: x.cost[0])
        return sel


class REGULAR:
    def selection(self, gen_arr, k):
        return [gen_arr[random.randint(0, int(GA_POPSIZE/2))] for i in range(k)]


def init_population(capacity, dist_matrix, goods):
    pop, buffer = [], []
    for i in range(GA_POPSIZE):
        pop.append(Genetic(capacity, dist_matrix, goods, np.random.permutation(range(1, len(goods)))))
        buffer.append(None)
    return pop, buffer     # arrays of Genetic type population and buffer initialized


# sorts population by key fitness value
def sort_by_fitness(gen_arr):
    gen_arr.sort(key=lambda x: x.cost[0])
    return gen_arr


# takes GA_ELITRATE percent to next generation
def elitism(gen_arr, buffer, esize, capacity, dist_matrix, goods):
    for i in range(esize):
        buffer[i] = Genetic(capacity, dist_matrix, goods, permutation=gen_arr[i].config)
    return buffer


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


class SwapMutation:
    def mutate(self, gen):
        index = random.sample(range(len(gen.goods)), 2)
        temp = gen.config[index[0] - 1]
        gen.config[index[0] - 1] = gen.config[index[1] - 1]
        gen.config[index[1] - 1] = temp


# scramble mutation as seen in word mutation file
class ScrambleMutation:
    def mutate(self, gen):
        index = random.sample(list(range(len(gen.goods))), 2)
        index.sort()
        start, end = index[0], index[1]
        gen.config[start:end] = np.random.permutation(gen.config[start:end])


##################################################################################################


# generic mating function
# supports elitism, aging, selection types, crossovers, possible string values, different target lengths
def mate(gen_arr, buffer, crossover_type, selection_type, mut_type, capacity, dist_matrix, goods, min_age=0):
    esize = int(GA_POPSIZE * GA_ELITRATE)       # number of elitism moving to next generation
    buffer = elitism(gen_arr, buffer, esize, capacity, dist_matrix, goods)  # filling buffer with best of this generation
    can_mate = ageing(gen_arr, min_age)         # generate possible parents

    # mating parents
    if len(can_mate) > 0:
        for i in range(esize, GA_POPSIZE):
            s = selection_type.selection(gen_arr, 2)
            mut = crossover_type.crossover(s[0], s[1])
            buffer[i] = Genetic(capacity, dist_matrix, goods, permutation=mut)

            # in GA_MUTATIONRATE chance new child will mutate
            if np.random.choice([True, False], p=[GA_MUTATIONRATE, 1-GA_MUTATIONRATE]):
                mut_type.mutate(buffer[i])
    return gen_arr, buffer


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
