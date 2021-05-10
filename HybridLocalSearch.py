import random
import numpy as np
import copy


class HybridLocalSearch:
    def __init__(self, graph, uncolored=False, random_coloring=False):
        self.graph = graph.__deepcopy__()
        self.domains = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V + 1)]
        self.nodes_with_color = [set() for _ in range(self.graph.k)]
        self.bad_edges = [[] for _ in range(self.graph.k)]
        self.fitness = 0
        if uncolored:
            if not random_coloring:
                self.greedy_coloring()
            else:
                self.random_coloring()
            self.fitness = self.objective_function()

    def __deepcopy__(self):
        new = HybridLocalSearch(self.graph.__deepcopy__())
        new.nodes_with_color = copy.deepcopy(self.nodes_with_color)
        new.domains = copy.deepcopy(self.domains)
        new.fitness = new.objective_function()
        return new

    def __str__(self):
        return "BEST K: " + str(self.graph.colors_used_until_now) + "\nFitness = " + str(self.fitness)

    def uncolor_node(self, node):
        color = node.color
        self.graph.uncolor_node(node)
        self.nodes_with_color[color].remove(node.number)
        for neigh in node.neighbors:
            self.domains[neigh.number][color] -= 1

    def color_node(self, node, color):
        if node.color is not None:
            self.uncolor_node(node)
        self.graph.color_node(node, color)

        self.nodes_with_color[color].add(node.number)

        for neigh in node.neighbors:
            self.domains[neigh.number][color] += 1

    def objective_function(self):
        for color in self.bad_edges:
            color.clear()
        for v1 in self.graph.nodes[1:]:
            for v2 in v1.neighbors:
                if v1.number < v2.number and v1.color == v2.color:
                    self.bad_edges[v1.color].append((v1.number, v2.number))

        i = 0
        while i < len(self.nodes_with_color)-1:
            if not self.nodes_with_color[i]:
                self.update_k()
            i += 1

        val = 0
        for color in range(self.graph.k):
            val += 2*len(self.bad_edges[color])*len(self.nodes_with_color[color]) - len(self.nodes_with_color[color])**2

        return -val

    def random_neighbor(self):
        new = self.__deepcopy__()
        random_node = random.choice(new.graph.nodes[1:])
        color_list = [i for i in range(new.graph.k) if i != random_node.color]
        random_color = random.choice(color_list)
        new.color_node(random_node, random_color)
        new.fitness = new.objective_function()
        return new

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

        for color in range(self.graph.k):
            if self.domains[node.number][color] > 0:
                all_colors[color] = -1

        for color in range(len(all_colors)):
            if self.domains[node.number][color] == 0:
                for neigh in neighbors:
                    if self.domains[neigh.number][color] > 0:
                        all_colors[color] += 1

        return np.argmax(all_colors)

    # finds initial coloring using greedy algorithm
    def greedy_coloring(self):
        while len(self.graph.uncolored_nodes) > 1:
            next_node = self.MRVandHD()
            color = self.get_colors_by_LCV(next_node)
            self.color_node(next_node, color)
        for i in range(len(self.domains)):
            self.domains[i] = self.domains[i][:self.graph.colors_used_until_now]
        self.nodes_with_color = self.nodes_with_color[:self.graph.colors_used_until_now]
        self.graph.k = self.graph.colors_used_until_now

    def random_coloring(self):
        for node in self.graph.nodes[1:]:
            random_color = random.choice(list(range(self.graph.k)))
            self.color_node(node, random_color)
        self.arrange_nodes()
        self.fitness = self.objective_function()
        for i in range(len(self.domains)):
            self.domains[i] = self.domains[i][:self.graph.colors_used_until_now]
        self.nodes_with_color = self.nodes_with_color[:self.graph.colors_used_until_now]
        self.graph.k = self.graph.colors_used_until_now

    def arrange_nodes(self):
        for color, color_set in enumerate(self.nodes_with_color):
            minimum_node = np.inf
            minimum_set = 0
            for j in range(color, len(self.nodes_with_color)):
                if self.nodes_with_color[j]:
                    min_node_temp = min(self.nodes_with_color[j])
                    if min_node_temp < minimum_node:
                        minimum_node = min_node_temp
                        minimum_set = j
            self.swap_colors(minimum_set, color)

    def swap_colors(self, color1, color2):
        temp1 = [node_number for node_number in self.nodes_with_color[color1]]
        temp2 = [node_number for node_number in self.nodes_with_color[color2]]
        for v in temp1:
            self.color_node(self.graph.nodes[v], color2)
        for v in temp2:
            self.color_node(self.graph.nodes[v], color1)

    def update_k(self):
        color = None
        for i, nodes_color in enumerate(self.nodes_with_color):
            if not nodes_color:
                color = i
                break

        if color is not None:
            last_color = 0
            for i, color_set in enumerate(self.nodes_with_color):
                if color_set:
                    last_color = i

            last_color_set = self.nodes_with_color[last_color].copy()
            for node_number in last_color_set:
                self.color_node(self.graph.nodes[node_number], color)

            self.graph.k = self.graph.colors_used_until_now
            for i in range(len(self.domains)):
                self.domains[i] = self.domains[i][:last_color]
            self.nodes_with_color = self.nodes_with_color[:last_color]
