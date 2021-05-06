import numpy as np
import sys
sys.setrecursionlimit(10000)


class BacktrackingWithBackjumping:
    def __init__(self, graph):
        self.graph = graph.__deepcopy__()
        # uses to keep track of conflicts entry time to conflict set
        self.conflict_counter = 1
        # all nodes conflict sets
        self.conflict_set = [[0 for _ in range(self.graph.V)] * self.graph.V]
        # domain of colors node tried using
        self.my_domains = [[True for _ in range(self.graph.k)] for _ in range(self.graph.V)]
        # domain of colors neighbors of nodes are colored in
        self.neighbors_constraints = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V)]

    # finds minimum remaining values variable with Highest Degree
    def MRVandHD(self):
        # calculates number of colors available for each node
        remaining_values = [0 for _ in range(self.graph.V)]
        for node in range(self.graph.V):
            for color in range(self.graph.k):
                if self.my_domains[node][color] and not self.neighbors_constraints[node][color]:
                    remaining_values[node] += 1

        # find the minimum number of values available
        min_remaining_values = min(remaining_values)
        # find all nodes with minimum number of values available
        nodes_min_remaining = [i for i in range(len(remaining_values)) if remaining_values[i] == min_remaining_values]
        # from nodes with minimum number of values, choose the node with the highest degree
        highest_degree = 0
        for node_number in nodes_min_remaining:
            if len(self.graph.nodes[node_number].neighbors) > highest_degree:
                best_node = self.graph.nodes[node_number]
                highest_degree = len(self.graph.nodes[node_number].neighbors)
        return best_node

    # finds least constraining color for "node"
    def get_colors_by_LCV(self, node):
        neighbors = node.neighbors
        all_colors = [0 for _ in range(self.graph.k)]
        best_color, constraints, best_constraint = None, 0, 0
        neighbors_colors = self.neighbors_constraints[node.number]
        tried_colors = self.my_domains[node.number]

        for color in range(len(all_colors)):
            if (tried_colors[color] is True) and (neighbors_colors[color] == 0):
                for neigh in neighbors:
                    if self.neighbors_constraints[neigh.number][color] != 0:
                        all_colors[color] += 1
            else:
                all_colors[color] = -1

        return all_colors

    # check for node_number if exists a color, if so color the node
    def try_to_color(self, node_number):
        # colors used in past by "node", and colors of "node"s neighbors
        try_colors = self.get_colors_by_LCV(self.graph.nodes[node_number])
        node_domain = self.my_domains[node_number]

        # iterating through nodes colors, if node didn't use color in past and neighbors not using color
        # than color is legal
        while not all(x == -1 for x in try_colors):
            # found legal color
            color = np.argmax(try_colors)
            try_colors[color] = -1
            node_domain[color] = False

            self.color_node(self.graph.nodes[node_number], color)
            return True
        return False

    # color "node" with "color"
    def color_node(self, node, color):
        # use graphs coloring function
        self.graph.color_node(node, color)

        # update conflict sets and neighbor constraints based on coloring
        for neigh in node.neighbors:
            self.conflict_set[neigh.number][node.number] = self.conflict_counter
            self.neighbors_constraints[neigh.number][color] += 1
        self.conflict_counter += 1

    # uncolor "node"
    def uncolor_node(self, node, color):
        # use graphs uncoloring function
        self.graph.uncolor_node(node)

        # update neighbor constraints
        for neighbor in node.neighbors:
            self.neighbors_constraints[neighbor.number][color] -= 1

    # backjump to position of no dead end
    def backjump(self, node_number):
        # choosing dead end node by conflict set
        last_conflict = np.argmax(self.conflict_set[node_number])
        # if node has no conflicts -> no legal coloring exists
        if last_conflict == 0:
            return False

        # update conflict set of current node and last conflicts nodes
        for i, conf in enumerate(self.conflict_set[node_number]):
            if conf and i != last_conflict:
                self.conflict_set[last_conflict][i] = conf
        self.conflict_set[node_number] = [0 for _ in range(self.graph.V)]

        # initialize current nodes domain
        self.my_domains[node_number] = [True for _ in range(len(self.graph.colors))]

        # remove color from dead end node
        lc_color = self.graph.nodes[last_conflict].color
        self.uncolor_node(self.graph.nodes[last_conflict], lc_color)

    # coloring search function
    def backtracking(self):
        while self.graph.uncolored_nodes:
            next_node_number = self.MRVandHD()
            if not self.try_to_color(next_node_number):
                if not self.backjump(next_node_number):
                    return False
        return True
