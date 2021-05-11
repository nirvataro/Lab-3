import random
import numpy as np
import copy


class FeasibleLocalSearch:
    def __init__(self, graph, uncolored=False, random_coloring=False):
        # legal graph with best k found
        self.graph = graph.__deepcopy__()
        self.highest_degree = max([len(node.neighbors) for node in self.graph.nodes[1:]])
        # illegal graph with k-1 colors, trying to make it legal
        self.try_graph = None
        # node color domains
        self.domains = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]
        # sets of nodes with same color
        self.nodes_with_color = [set() for _ in range(self.graph.k)]
        # for SA an GA initial coloring
        if uncolored:
            if not random_coloring:
                self.greedy_coloring()
            else:
                self.random_coloring()
            # update k based on coloring we found
            self.update_k()
            # initializes try_graph
            self.try_one_color_less()
        # fitness refers to try_graph coloring
        self.fitness = 0

    def __deepcopy__(self):
        new = FeasibleLocalSearch(self.graph.__deepcopy__())
        new.domains = copy.deepcopy(self.domains)
        new.fitness = new.objective_function()
        return new

    # finds minimum remaining values variable with Highest Degree
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

    # colors a node and updates domains
    def color_node(self, node, color):
        if node.color is not None:
            self.uncolor_node(node)
        self.graph.color_node(node, color)

        self.nodes_with_color[color].add(node.number)

        for neigh in node.neighbors:
            self.domains[neigh.number][color] += 1

    # uncolors a node and updates domains
    def uncolor_node(self, node):
        color = node.color
        self.graph.uncolor_node(node)

        self.nodes_with_color[color].remove(node.number)

        for neigh in node.neighbors:
            self.domains[neigh.number][color] -= 1

    # finds initial coloring using greedy algorithm
    def greedy_coloring(self):
        while len(self.graph.uncolored_nodes) > 1:
            next_node = self.MRVandHD()
            color = self.get_colors_by_LCV(next_node)
            self.color_node(next_node, color)

    def random_coloring(self):
        for node in self.graph.nodes:
            random_color = random.choice(list(range(self.graph.k)))
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

    #
    def objective_function(self):
        value = self.highest_degree + 2
        value -= self.try_graph.k
        value *= self.try_graph.V
        for v1 in self.try_graph.nodes:
            for v2 in v1.neighbors:
                if v1.number < v2.number and v1.color == v2.color:
                    value -= 1
        return value

    def find_bad_nodes(self):
        bad_nodes = set()
        for v1 in self.graph.nodes:
            for v2 in v1.neighbors:
                if v1.color == v2.color:
                    bad_nodes.add(v1)
                    bad_nodes.add(v2)
        return list(bad_nodes)

    def random_neighbor(self):
        random_node = random.choice(self.graph.nodes[1:])
        node_degree = len(random_node.neighbors)
        np_neighbors_colors = np.array(self.domains[random_node.number])
        np_neighbors_colors[random_node.color] = node_degree
        prob = node_degree - np_neighbors_colors
        prob = prob / sum(prob)

        color_list = list(range(self.graph.k))
        new_color = np.random.choice(color_list, p=prob)
        new_graph = self.graph.__deepcopy__()
        new_graph_obj = FeasibleLocalSearch(new_graph)
        print(new_color)
        print(random_node)
        new_graph_obj.color_node(random_node, new_color)
        new_graph_obj.fitness = new_graph_obj.objective_function()

        return new_graph_obj

    # updates to new k when smaller coloring is found
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

    def try_one_color_less(self):
        less_color_graph = self.graph.__deepcopy__()
        less_color_graph.k = less_color_graph.colors_used_until_now - 1

        # all nodes with color k will be assigned a new color
        nodes_with_bad_color = self.nodes_with_color[-1]
        for node_number in nodes_with_bad_color:
            new_color = random.choice(list(range(less_color_graph.k)))
            self.color_node(less_color_graph.nodes[node_number], new_color)

        # we remove the last cell because color k was removed from color list
        for i in range(len(self.domains)):
            self.domains[i] = self.domains[i][:-1]
        self.nodes_with_color = self.nodes_with_color[:-1]

        self.try_graph = less_color_graph
        # calculate the fitness of try_graph
        self.fitness = self.objective_function()

    def legal(self):
        for v1 in self.try_graph.nodes:
            for v2 in v1.neighbors:
                if v1.color == v2.color:
                    return False
        return True

    def random_color(self):
        for node in self.graph.nodes[1:]:
            self.color_node(node, 0)
        self.fitness = self.objective_function()
