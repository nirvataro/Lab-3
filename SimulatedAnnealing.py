import time
import random
import numpy as np
from psutil import cpu_freq
from Objective_local_search import ObjectiveFunctionGraph


class SimulatedAnnealing:
    def __init__(self, graph, search_time=120, output=False):
        self.saBest = ObjectiveFunctionGraph(graph.__deepcopy__())
        self.saBest.graph.initial_solution()
        self.sa_search(search_time, output)

    # SA search method
    def sa_search(self, search_time, output):
        candidate = self.saBest
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        i = 0
        while time_left > 0:
            # temperature is proportional to time left
            temp = 90 * time_left / search_time
            random_neighbor = self.getRandomNeighborhood(candidate)

            candidate_of = candidate.objective_function()
            random_neighbor_of = random_neighbor.objective_function()
            saBest_of = self.saBest.objective_function()
            # avoid underflow
            if temp < 0.01:
                chance = 0
            else:
                chance = np.exp((random_neighbor_of - candidate_of) / temp)
            # new best found
            if random_neighbor_of > saBest_of:
                self.saBest = random_neighbor
                if output:
                    print("Improvement Found!")
                    print("Best:")
                    print(self.saBest)
                    total_time = search_time-time_left
                    print("Elapsed Time: ", total_time)
                    print("Total clock ticks: ", total_time * cpu_freq()[0] * 2 ** 20)
                    print("Total iteration: ", i, "\n")

            if random_neighbor_of > candidate_of or random.random() < chance:
                candidate = random_neighbor
            i += 1
            time_left = end_time - time.time()

    # returns one random neighbor of current graph
    def getRandomNeighborhood(self, candidate):
        color = random.choice(range(len(self.saBest.graph.colors)))
        nodes = [node.number for node in self.saBest.graph.nodes if node.color != color]
        node = random.choice(nodes)
        neigh = ObjectiveFunctionGraph(candidate.graph.__deepcopy__())
        neigh.kempe_chains(self.saBest.graph.nodes[node], color)
        return neigh

    # print method
    def __str__(self):
        string = "Simulated Annealing:\n"
        return string + str(self.saBest)
