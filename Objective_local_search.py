import random
import numpy as np
import copy


class ObjectiveLocalSearch:
    def __init__(self, graph, uncolored=False, random_coloring=False):
        self.graph = graph.__deepcopy__()
        self.domains = [[0 for _ in range(self.graph.k)] for j in range(self.graph.V + 1)]
        self.nodes_with_color = [set() for _ in range(self.graph.k)]
        self.fitness = 0
        if uncolored:
            if not random_coloring:
                self.greedy_coloring()
            else:
                self.random_coloring()
            self.fitness = self.objective_function()

    def __deepcopy__(self):
        new = ObjectiveLocalSearch(self.graph.__deepcopy__())
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
        val = sum([len(color)**2 for color in self.nodes_with_color])
        return val

    def kempe_chains(self, node, new_color):
        new = self.__deepcopy__()
        true_new_color = new_color
        old_color_nodes = set()
        new_color_nodes = set()
        old_color = node.color
        new_nodes = [node.number]
        while new_nodes:
            neighbors = []
            for node_number in new_nodes:
                neighbors += [v.number for v in new.graph.nodes[node_number].neighbors if v.color == new_color]
                old_color_nodes.add(node_number)
            new_nodes = []
            for v in neighbors:
                if v not in new_color_nodes:
                    new_nodes.append(v)
            old_color, new_color = new_color, old_color
            old_color_nodes, new_color_nodes = new_color_nodes, old_color_nodes
        if true_new_color != new_color:
            old_color, new_color = new_color, old_color
            old_color_nodes, new_color_nodes = new_color_nodes, old_color_nodes
        for v in old_color_nodes:
            new.color_node(new.graph.nodes[v], new_color)
        for v in new_color_nodes:
            new.color_node(new.graph.nodes[v], old_color)

        new.fitness = new.objective_function()
        for nodes_color in new.nodes_with_color:
            if not nodes_color:
                new.update_k()

        return new

    def random_neighbor(self):
        random_node = random.choice(self.graph.nodes[1:])
        color_list = [i for i in range(self.graph.k) if i != random_node.color]
        nodes_with_random_node_color = len(self.nodes_with_color[random_node.color])
        total_nodes = self.graph.V - nodes_with_random_node_color
        prob = np.array([len(nodes) for i, nodes in enumerate(self.nodes_with_color) if i != random_node.color])
        prob = prob / sum(prob)
        random_color = np.random.choice(color_list, p=prob)
        return self.kempe_chains(random_node, random_color)

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
        for node in self.graph.nodes:
            color_list = [i for i in self.domains[node.number] if self.domains[node.number][i]==0]
            random_color = random.choice(color_list)
            self.color_node(node, random_color)
        self.arrange_nodes()
        self.fitness = self.objective_function()

    def arrange_nodes(self):
        for color, color_set in enumerate(self.nodes_with_color):
            minimum_node = np.inf
            minimum_set = 0
            for j in range(color, len(self.nodes_with_color)):
                min_node_temp = min(self.nodes_with_color[j])
                if min_node_temp < minimum_node:
                    minimum_node = min_node_temp
                    minimum_set = j
            self.swap_colors(minimum_set, color)

    def swap_colors(self, color1, color2):
        temp = [node_number for node_number in self.nodes_with_color[color1]]
        for v in self.nodes_with_color[color1]:
            self.color_node(self.graph.nodes[v], color2)
        for v in temp:
            self.color_node(self.graph.nodes[v], color1)

    def update_k(self):
        print("found smaller k")
        for i, nodes_color in enumerate(self.nodes_with_color):
            if not nodes_color:
                color = i
                break

        for node in self.graph.nodes[1:]:
            if node.color == self.graph.k:
                self.color_node(node, color)

        self.nodes_with_color[color] = self.nodes_with_color[self.graph.k-1]

        self.graph.k = self.graph.colors_used_until_now
        for i in range(len(self.domains)):
            self.domains[i] = self.domains[i][:self.graph.k]
        self.nodes_with_color = self.nodes_with_color[:self.graph.k]
