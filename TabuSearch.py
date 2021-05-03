from MetaHeuristicFramework import VRP
import numpy as np
import random
import time
from psutil import cpu_freq


class TabuSearch:
    def __init__(self, capacity, dist_matrix, goods, maxTabuSize=None, search_time=120, output=False):
        self.tabu_list = {}
        self.cities = list(range(1, len(goods)))
        self.city_dist_matrix = dist_matrix
        self.goods = goods
        self.truck_capacity = capacity
        self.tsBest = VRP(capacity, dist_matrix, goods)
        self.tabu_list[self.tsBest.config.tobytes()] = 0
        if maxTabuSize is None or maxTabuSize > len(self.cities) ** 2:
            maxTabuSize = round(len(self.cities) ** 2)
        self.t_search(search_time, maxTabuSize, output)

    # TABU search function
    def t_search(self,  search_time, t_size, output):
        best_candidate = self.tsBest
        last_improved = 1
        end_time = time.time() + search_time
        time_left = end_time - time.time()
        i = 0
        while time_left > 0:
            neighborhood = self.getNeighborhood(best_candidate)
            best_candidate = None
            # find candidate
            for cand in neighborhood:
                if self.tabu_list.get(cand.config.tobytes()) is None and (best_candidate is None or best_candidate.cost[0] > cand.cost[0]):
                    best_candidate = cand
            # init
            if best_candidate is None:
                max_t = 0
                for cand in self.tabu_list:
                    if self.tabu_list[cand] > max_t:
                        best_config = np.fromstring(cand, dtype=int)
                        best_candidate = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, best_config)
                        max_t = self.tabu_list[cand]
                self.tabu_list.pop(best_config.tobytes())
            # new best found
            if best_candidate.cost[0] < self.tsBest.cost[0]:
                if output:
                    self.tsBest = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, config=best_candidate.config.copy())
                    print("Improvement Found!")
                    print("Best:")
                    print(self.tsBest)
                    total_time = search_time-time_left
                    print("Elapsed Time: ", total_time)
                    print("Total clock ticks: ", total_time * cpu_freq()[0] * 2 ** 20)
                    print("Total iteration: ", i, "\n")
                last_improved = 1
            else:
                last_improved += 1
            self.tabu_list[best_candidate.config.tobytes()] = 0
            for tenure in self.tabu_list.keys():
                self.tabu_list[tenure] += 1
            # tabu passed limit
            if len(self.tabu_list) > t_size:
                key_to_delete = max(self.tabu_list, key=lambda k: self.tabu_list[k])
                del self.tabu_list[key_to_delete]
            # random mutation
            if not last_improved % 100:
                if output:
                    print("Mutation ")
                best_candidate = self.mutate()
            # random reset
            if last_improved == 300:
                if output:
                    print("Random Reset")
                city_list = self.cities.copy()
                best_candidate = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, config=random.shuffle(city_list))
                last_improved = 0
            i += 1
            time_left = end_time - time.time()

    # print function
    def __str__(self):
        string = "Tabu Search:\nThe Best Route Found: \n"
        return string + str(self.tsBest)

    # returns all neighbors of candidate
    def getNeighborhood(self, candidate):
        neighborhood = []
        for i in range(len(candidate.config)):
            for j in range(i+1, len(candidate.config)):
                new_node = [i for i in candidate.config]
                new_node[i], new_node[j] = new_node[j], new_node[i]
                neighborhood.append(VRP(self.truck_capacity, self.city_dist_matrix, self.goods, np.array(new_node)))
        return neighborhood

    # finds new similar permutation that is not in TABU, or returns new permutation
    def mutate(self):
        for _ in range(15):
            s_points = random.sample(range(len(self.tsBest.config)), 2)
            s_points.sort()
            start, end = s_points[0], s_points[1]
            part = self.tsBest.config[start:end].copy()
            random.shuffle(part)
            new_config = self.tsBest.config.copy()
            new_config[start:end] = part
            best_candidate = VRP(self.truck_capacity, self.city_dist_matrix, self.goods, new_config)
            if self.tabu_list.get(best_candidate.config.tobytes()) is None:
                return best_candidate
        city_list = self.cities.copy()
        return VRP(self.truck_capacity, self.city_dist_matrix, self.goods, config=random.shuffle(city_list))
