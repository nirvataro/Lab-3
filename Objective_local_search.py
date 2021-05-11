import random
import numpy as np
import copy


class ObjectiveLocalSearch:
    def __init__(self, graph, uncolored=False, random_coloring=False):
        # the graph we will try to color
        self.graph = graph.__deepcopy__()
        # domain of each node
        self.domains = [[0 for _ in range(self.graph.k)] for j in range(self.graph.V + 1)]
        # color sets of nodes with the same color
        self.nodes_with_color = [set() for _ in range(self.graph.k)]
        # graph objective function value
        self.fitness = 0
        # when trying to improve a graph we will create a copy of the graph and improve it
        if uncolored:
            if not random_coloring:
                self.greedy_coloring()
            else:
                # for GA
                self.random_coloring()
            self.fitness = self.objective_function()

    # copy method
    def __deepcopy__(self):
        new = ObjectiveLocalSearch(self.graph.__deepcopy__())
        new.nodes_with_color = copy.deepcopy(self.nodes_with_color)
        new.domains = copy.deepcopy(self.domains)
        new.fitness = new.objective_function()
        return new

    # print method
    def __str__(self):
        return "Best K: " + str(self.graph.colors_used_until_now) + "\nFitness = " + str(self.fitness)

    # removes color from "node"
    def uncolor_node(self, node):
        color = node.color
        self.graph.uncolor_node(node)

        # update domains and nodes with color
        self.nodes_with_color[color].remove(node.number)
        for neigh in node.neighbors:
            self.domains[neigh.number][color] -= 1

    # colors "node" with "color"
    def color_node(self, node, color):
        # if node already colored, first remove it's color
        if node.color is not None:
            self.uncolor_node(node)
        self.graph.color_node(node, color)

        # update domains and nodes with color
        self.nodes_with_color[color].add(node.number)
        for neigh in node.neighbors:
            self.domains[neigh.number][color] += 1

    # calculates graph fitness as seen in lecture
    def objective_function(self):
        val = sum([len(color)**2 for color in self.nodes_with_color])
        return val

    # creates kempe chain from lecture given a node and a color
    def kempe_chains(self, node, new_color):
        new = self.__deepcopy__()
        # the true color we want to color "node" in
        true_new_color = new_color

        # sets of nodes in the chain of each color
        old_color_nodes = set()
        new_color_nodes = set()
        old_color = node.color

        # will hold the nodes that have yet to add their neighbors to chain
        new_nodes = [node.number]
        while new_nodes:
            neighbors = []
            # add all neighbors of nodes in "new_nodes" that are in opposite color to neighbors array
            for node_number in new_nodes:
                neighbors += [v.number for v in new.graph.nodes[node_number].neighbors if v.color == new_color]
                old_color_nodes.add(node_number)
            new_nodes = []
            # of all neighbors that were found, keep only the ones who were yet to be seen
            for v in neighbors:
                if v not in new_color_nodes:
                    new_nodes.append(v)
            # swap between colors to continue chain
            old_color, new_color = new_color, old_color
            old_color_nodes, new_color_nodes = new_color_nodes, old_color_nodes

        # swap colors once more if inconsistent
        if true_new_color != new_color:
            old_color, new_color = new_color, old_color
            old_color_nodes, new_color_nodes = new_color_nodes, old_color_nodes
        # coloring all nodes with "old color" in "new color"
        for v in old_color_nodes:
            new.color_node(new.graph.nodes[v], new_color)
        # same backwards
        for v in new_color_nodes:
            new.color_node(new.graph.nodes[v], old_color)

        # calculate the new fitness
        new.fitness = new.objective_function()

        # update k if needed
        for nodes_color in new.nodes_with_color:
            if not nodes_color:
                new.update_k()

        return new

    # generates a random neighbor of graph for SA
    def random_neighbor(self):
        random_node = random.choice(self.graph.nodes[1:])
        color_list = [i for i in range(self.graph.k) if i != random_node.color]
        prob = np.array([len(nodes) for i, nodes in enumerate(self.nodes_with_color) if i != random_node.color])
        prob = prob / sum(prob)
        random_color = np.random.choice(color_list, p=prob)
        return self.kempe_chains(random_node, random_color)

    # for greedy coloring
    def MRVandHD(self):
        # calculates number of colors available for each node
        remaining_values = [0 for _ in range(self.graph.V+1)]
        for node in self.graph.uncolored_nodes:
            for color in range(self.graph.k):
                if self.domains[node.number][color] == 0:
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

    # for GA
    def random_coloring(self):
        for node in self.graph.nodes:
            color_list = [i for i in self.domains[node.number] if self.domains[node.number][i]==0]
            random_color = random.choice(color_list)
            self.color_node(node, random_color)
        self.arrange_nodes()
        self.fitness = self.objective_function()

    # arranges colors for consistency when trying to crossover between graphs
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

    # auxiliary function
    def swap_colors(self, color1, color2):
        temp = [node_number for node_number in self.nodes_with_color[color1]]
        for v in self.nodes_with_color[color1]:
            self.color_node(self.graph.nodes[v], color2)
        for v in temp:
            self.color_node(self.graph.nodes[v], color1)

    # updates to new k when smaller coloring is found
    def update_k(self):
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
