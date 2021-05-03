import numpy as np
import random
from MetaHeuristicFramework import VRP
import time
from psutil import cpu_freq


class SimulatedAnnealing:
    def __init__(self, capacity, dist_matrix, goods, search_time=120, output=False):
        self.saBest = VRP(capacity, dist_matrix, goods)
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
            # avoid underflow
            if temp < 0.01:
                chance = 0
            else:
                chance = np.exp((candidate.cost[0] - random_neighbor.cost[0]) / temp)
            # new best found
            if random_neighbor.cost[0] < self.saBest.cost[0]:
                self.saBest = random_neighbor
                if output:
                    print("Improvement Found!")
                    print("Best:")
                    print(self.saBest)
                    total_time = search_time-time_left
                    print("Elapsed Time: ", total_time)
                    print("Total clock ticks: ", total_time * cpu_freq()[0] * 2 ** 20)
                    print("Total iteration: ", i, "\n")

            if random_neighbor.cost[0] < candidate.cost[0] or random.random() < chance:
                candidate = random_neighbor
            i += 1
            time_left = end_time - time.time()

    # returns one random neighbor of current config
    def getRandomNeighborhood(self, candidate):
        index_ij = random.sample(self.cities, 2)
        index_ij.sort()
        i_ind, j_ind = index_ij[0] - 1, index_ij[1] - 1
        neigh_config = candidate.config.copy()
        neigh_config[j_ind], neigh_config[i_ind] = candidate.config[i_ind], candidate.config[j_ind]
        return VRP(self.truck_capacity, self.city_dist_matrix, self.goods, neigh_config)

    # print method
    def __str__(self):
        string = "Simulated Annealing:\nThe Best Route Found: \n"
        return string + str(self.saBest)
