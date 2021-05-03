import numpy as np
import random


# solution class
class VRP:
    def __init__(self, capacity, dist_matrix, goods, config=None):
        self.trucks = [Truck(capacity)]
        self.max_capacity = capacity
        self.dist_matrix = dist_matrix
        self.goods = goods
        self.unvisited_cities = list(range(1, len(goods)))
        if config is None:
            self.config = self.generate_start_permutation_3NN()
        else:
            self.config = config
        self.cost = None
        self.update_path()

    # adds new truck if needed
    def add_truck(self):
        self.trucks.append(Truck(self.max_capacity))

    # adds next city to route
    def add_route(self, city):
        if self.trucks[-1].capacity - self.goods[city] < 0:
            self.trucks[-1].distance_travel += self.dist_matrix[self.trucks[-1].route[-1]][0]
            self.trucks[-1].route.append(0)
            self.add_truck()

        self.trucks[-1].capacity -= self.goods[city]
        self.trucks[-1].distance_travel += self.dist_matrix[self.trucks[-1].route[-1]][city]
        self.trucks[-1].route.append(city)
        if city != 0:
            self.unvisited_cities.remove(city)

    # cost of configuration function
    def calc_cost(self):
        total_cost = 0
        # basic cost
        for t in self.trucks:
            total_cost += t.distance_travel
        # improving configuration
        for i in range(len(self.trucks) - 1):
            last_city = self.trucks[i].route[-2]
            if self.trucks[i+1].capacity - self.goods[last_city] > 0 and self.dist_matrix[last_city][self.trucks[i].route[-3]] + self.dist_matrix[0][self.trucks[i].route[-3]] > self.dist_matrix[self.trucks[i+1].route[1]][last_city] + self.dist_matrix[0][last_city]:
                self.trucks[i].route.remove(last_city)
                self.trucks[i].distance_travel = self.trucks[i].distance_travel - self.dist_matrix[last_city][0] - self.dist_matrix[last_city][self.trucks[i].route[-2]] + self.dist_matrix[self.trucks[i].route[-2]][0]
                self.trucks[i].capacity += self.goods[last_city]
                self.trucks[i+1].route.insert(1, last_city)
                self.trucks[i+1].distance_travel = self.trucks[i+1].distance_travel - self.dist_matrix[0][self.trucks[i+1].route[2]] + \
                                                 self.dist_matrix[self.trucks[i+1].route[0]][self.trucks[i+1].route[1]] + self.dist_matrix[self.trucks[i+1].route[1]][self.trucks[i+1].route[2]]
                self.trucks[i+1].capacity -= self.goods[last_city]
                return self.calc_cost()
        return total_cost, len(self.trucks)

    # update trucks path
    def update_path(self):
        self.trucks = [Truck(self.max_capacity)]
        for city in self.config:
            self.add_route(city)
        self.add_route(0)
        self.cost = self.calc_cost()
        self.unvisited_cities = list(range(1, len(self.goods)))

    # print method
    def __str__(self):
        string = "Route: \n"
        for i, t in enumerate(self.trucks):
            string += "Truck: {} ".format(str(i + 1)) + str(t) + "\n"
        return string + "Total Cost: " + str(self.cost)

    # init method of first route (if not given)
    def generate_start_permutation_3NN(self):
        permutation = []
        unvisited_cities = self.unvisited_cities.copy()
        cities = self.unvisited_cities.copy()
        current_city = 0
        while unvisited_cities:
            min1 = min2 = min3 = np.inf
            min1_city, min2_city, min3_city = 0, 0, 0
            for city in cities:
                dist = self.dist_matrix[current_city][city]
                if city != current_city and dist < min3 and city in unvisited_cities and city != 0:
                    min3 = dist
                    min3_city = city
                    if dist < min2:
                        min3, min2 = min2, min3
                        min3_city, min2_city = min2_city, min3_city
                        if min2 < min1:
                            min1, min2 = min2, min1
                            min1_city, min2_city = min2_city, min1_city
            choices = [min1_city, min2_city, min3_city]
            choices = list(filter(lambda x: x != 0, choices))
            city = random.choice(choices)
            permutation.append(city)
            unvisited_cities.remove(city)
        return np.array(permutation)


# truck object
class Truck:
    def __init__(self, capacity):
        self.capacity = capacity
        self.distance_travel = 0
        self.route = [0]

    # print function
    def __str__(self):
        return str(self.route) + " Capacity left: " + str(self.capacity)
