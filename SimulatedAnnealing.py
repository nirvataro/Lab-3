import time
import random
import numpy as np
from psutil import cpu_freq


class SimulatedAnnealing:
    def __init__(self, search_graph):
        self.saBest = search_graph
        self.iterations = 0

    # SA search method
    def sa_search(self, search_time=120, output=False):
        candidate = self.saBest.__deepcopy__()
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        while time_left > 0:
            # temperature is proportional to time left
            temp = 90 * time_left / search_time
            random_neighbor = self.saBest.random_neighbor()
            if random_neighbor is None:
                return
            # avoid underflow
            if temp < 0.01:
                chance = 0
            else:
                chance = np.exp((random_neighbor.fitness - candidate.fitness) / temp)
            # new best found
            if random_neighbor.fitness > self.saBest.fitness:
                self.saBest = random_neighbor
                self.saBest.objective_function()
                if output:
                    print("Improvement Found!")
                    print("Fitness: ", str(self.saBest.fitness))
                    print("Current Best K is {}".format(self.saBest.graph.colors_used_until_now))
                    total_time = search_time-time_left
                    print("Elapsed Time: ", total_time)
                    print("Total clock ticks: ", total_time * cpu_freq()[0] * 2 ** 20)
                    print("Total iteration: ", self.iterations, "\n")

            if random_neighbor.fitness > candidate.fitness or random.random() < chance:
                candidate = random_neighbor
            self.iterations += 1
            time_left = end_time - time.time()

    # print method
    def __str__(self):
        string = "Simulated Annealing:\n"
        return string + str(self.saBest)
