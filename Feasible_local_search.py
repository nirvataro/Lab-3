from LocalSeachGraph import LocalSearchGraph
import random
import SimulatedAnnealing as SA
import numpy as np


class FeasibleLocalSearch:
    def __init__(self, graph):
        self.graph = graph.__deepcopy__()
        self.greedy_coloring()
        self.domains = [[0 for _ in range(self.graph.k)] for j in range(self.graph.V+1)]
        self.greedy_coloring()

    # finds minimum remaining values variable with Highest Degree
    def MRVandHD(self):
        # calculates number of colors available for each node
        remaining_values = [0 for _ in range(self.graph.V+1)]
        for node in self.graph.uncolored_nodes:
            for color in range(self.graph.k):
                if self.domains[node.number][color]:
                    remaining_values[node.number] += 1

        # find the minimum number of values available
        remaining_values[0] = np.inf
        min_remaining_values = np.inf
        for node in self.graph.uncolored_nodes:
            if node.number != 0 and remaining_values[node.number] < min_remaining_values:
                min_remaining_values = remaining_values[node.number]

        # find all nodes with minimum number of values available
        nodes_min_remaining = []
        for i in range(len(remaining_values)):
            for uncolored_node in self.graph.uncolored_nodes:
                if (remaining_values[i] == min_remaining_values) and (uncolored_node.number == i):
                    nodes_min_remaining.append(i)

        # from nodes with minimum number of values, choose the node with the highest degree
        highest_degree = -1
        for node_number in nodes_min_remaining:
            if len(self.graph.nodes[node_number].neighbors) > highest_degree:
                best_node = self.graph.nodes[node_number]
                highest_degree = len(self.graph.nodes[node_number].neighbors)
        return best_node

    # finds least constraining color for "node"
    def get_colors_by_LCV(self, node):
        neighbors = node.neighbors
        all_colors = [0 for _ in range(self.graph.k)]

        for color in range(len(all_colors)):
            for neigh in neighbors:
                if self.domains[neigh.number][color] > 0:
                    all_colors[color] += 1

        return np.argmax(all_colors)

    # colors a node and updates domains
    def color_node(self, node, color):
        self.graph.color_node(node, color)

        for neigh in node.neighbors:
            self.domains[neigh.number][color] += 1

    # uncolors a node and updates domains
    def uncolor_node(self, node, color):
        self.graph.color_node(node)

        for neigh in node.neighbors:
            self.domains[neigh.number][color] -= 1

    # finds initial coloring using greedy algorithm
    def greedy_coloring(self):
        while len(self.graph.uncolored_nodes) > 1:
            next_node = self.MRVandHD()
            color = self.get_colors_by_LCV(next_node)
            self.color_node(next_node, color)

    def objective_function(self):
        function_value = 0
        for v1 in self.graph.nodes:
            valid = 1
            for v2 in v1.neighbors:
                if v1.color == v2.color:
                    valid = 0
                    break
            function_value += valid * self.domains[v1.number].count(0)

        return function_value

    def random_neighbor(self):
        random_node = random.choice(self.graph.nodes)
        node_degree = len(random_node.neighbors)
        np_neighbors_colors = np.array(self.domains[random_node.number])
        np_neighbors_colors[random_node.color] = node_degree
        prob = node_degree - np_neighbors_colors
        prob = np_neighbors_colors / sum(np_neighbors_colors)

        new_color = np.random.choice(list(range(self.graph.k)), p=prob)

    def try_one_color_less(self):


# def feasable_local_search(graph):
#     # find initial solution
#     k = graph.initial_solution()
#
#     # remove 1 color
#     graph.smaller_domain()
#     for node in graph.nodes:
#         if node.color is None:
#             graph.color_node(node, random.choice(list(range(k-1))))
