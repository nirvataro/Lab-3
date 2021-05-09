import time
import random
import numpy as np
from psutil import cpu_freq


class SimulatedAnnealing:
    def __init__(self, search_graph, search_time=120, output=False):
        self.saBest = search_graph
        self.sa_search(search_time, output)

    # SA search method
    def sa_search(self, search_time, output):
        candidate = self.saBest.__deepcopy__()
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        i = 0
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
                    print("Best:")
                    print(self.saBest.fitness)
                    # self.saBest.graph.draw()
                    total_time = search_time-time_left
                    print("")
                    print("Elapsed Time: ", total_time)
                    print("Total clock ticks: ", total_time * cpu_freq()[0] * 2 ** 20)
                    print("Total iteration: ", i, "\n")

            if random_neighbor.fitness > candidate.fitness or random.random() < chance:
                candidate = random_neighbor
            i += 1
            time_left = end_time - time.time()

    # print method
    def __str__(self):
        string = "Simulated Annealing:\n"
        return string + str(self.saBest)
