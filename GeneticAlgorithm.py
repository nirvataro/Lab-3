import random
import time
import numpy as np
from psutil import cpu_freq
from HybridLocalSearch import HybridLocalSearch as HLS
from Objective_local_search import ObjectiveLocalSearch as OLS
from Feasible_local_search import FeasibleLocalSearch as FLS


############## constants ###############
GA_POPSIZE = 1000        # ga population size
GA_ELITRATE = .2		    # elitism rate
GA_MUTATIONRATE = .25      # mutation rate
########################################


class GeneticAlgorithm:
    def __init__(self, graph, type='HLS',popsize=GA_POPSIZE, elite_rate=GA_ELITRATE, mutation_rate=GA_MUTATIONRATE):
        typeDictionary = {'HLS': HLS, 'OLS': OLS, 'FLS': FLS}
        self.local_search_type = typeDictionary[type]
        self.empty_graph = graph
        self.pop_size = popsize
        self.elite_size = round(elite_rate*popsize)
        self.mutation_rate = mutation_rate
        self.gen_arr, self.buffer = self.init_population()
        self.ages = [random.randint(0, 4) for _ in range(self.pop_size)]
        self.best_fitness = 0

    def __str__(self):
        output = ""
        output += "Genetic Algorithm:\n"
        output += str(self.gen_arr[0])
        output += "\nAvg fitness of gen: {}".format(self.avg_fit())
        output += "\nFitness STD: {}".format(self.std_fit())

        return output

    def init_population(self):
        gen_arr = [self.local_search_type(self.empty_graph, uncolored=True, random_coloring=True) for _ in range(self.pop_size)]
        buffer = [None for _ in range(self.pop_size)]
        return gen_arr, buffer

    # sorts population by key fitness value
    def sort_by_fitness(self, timer):
        self.gen_arr.sort(key=lambda x: x.fitness, reverse=True)
        if self.gen_arr[0].fitness > self.best_fitness:
            self.best_fitness = self.gen_arr[0].fitness
            print(self)
            iter_time = time.time() - timer
            print("Total time of generation: {}".format(iter_time))
            print("Total clock ticks (CPU)) of generation: {}\n".format(iter_time * cpu_freq()[0] * (2 ** 20)))

    # takes GA_ELITRATE percent to next generation
    def elitism(self):
        for i in range(self.elite_size):
            self.buffer[i] = self.gen_arr[i].__deepcopy__()

    def crossover(self, gen1, gen2):
        newgen = self.local_search_type(self.empty_graph)
        for node_number in range(self.empty_graph.V):
            color1 = gen1.graph.nodes[node_number].color
            color2 = gen2.graph.nodes[node_number].color
            color = random.choice([color1, color2])
            newgen.color_node(newgen.graph.nodes[node_number], color)
        newgen.arrange_nodes()
        newgen.fitness = newgen.objective_function()
        return newgen

    # RWS selection
    def selection(self, can_mate):
        # sel will store selected parents to mate
        total_fitness = sum([gen.fitness for gen in can_mate])

        # randomize a number between 0-sum of all fitness, find where that gen is and use as parent
        ran_selection = random.uniform(0, total_fitness)
        current, j = 0, 0
        while current < ran_selection:
            current += can_mate[j].fitness
            j += 1
        parent1 = can_mate[j]
        # randomize a number between 0-sum of all fitness, find where that gen is and use as parent
        ran_selection = random.uniform(0, total_fitness)
        current, j = 0, 0
        while current < ran_selection:
            current += can_mate[j].fitness
            j += 1
        parent2 = can_mate[j]
        return parent1, parent2

    def mutate(self, gen):
        return gen.random_neighbor()

    def mate(self):
        self.elitism()
        for i, age in enumerate(self.ages):
            self.ages[i] += 1

        can_mate = self.can_mate()

        # mating parents
        for i in range(self.elite_size, self.pop_size):
            p1, p2 = self.selection(can_mate)
            self.buffer[i] = self.crossover(p1, p2)

            # in GA_MUTATIONRATE chance new child will mutate
            if random.random() <= self.mutation_rate:
                self.buffer[i] = self.mutate(self.buffer[i])
        self.buffer, self.gen_arr = self.gen_arr, self.buffer

    def can_mate(self):
        can_mate = []
        for i, gen in enumerate(self.gen_arr):
            if self.ages[i] >= 3:
                can_mate.append(gen)
        return can_mate

    def avg_fit(self):
        fit_arr = [g.fitness for g in self.gen_arr]
        return np.mean(fit_arr)

    def std_fit(self):
        fit_arr = [g.fitness for g in self.gen_arr]
        return np.std(fit_arr)

    def genetic(self, search_time=120):
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        total_timer = time.time()
        i = 0
        while time_left > 0:
            gen_timer = time.time()

            self.sort_by_fitness(gen_timer)
            self.mate()

            time_left = end_time - time.time()
            i += 1

        total_time = time.time() - total_timer
        print("Total time : {}\nTotal clock ticks : {}\nTotal iterations:{}".format(total_time, total_time * cpu_freq()[
            0] * 2 ** 20, i + 1))

