import numpy as np
import sys
sys.setrecursionlimit(10000)


class BacktrackingWithBackjumping:
    def __init__(self, graph):
        self.graph = graph.__deepcopy__()
        # uses to keep track of conflicts entry time to conflict set
        self.conflict_counter = 1
        self.coloring_time = [np.inf for _ in range(self.graph.V+1)]
        # all nodes conflict sets
        self.conflict_set = [[0 for _ in range(self.graph.V+1)] for _ in range(self.graph.V+1)]
        # domain of colors node tried using
        self.my_domains = [[True for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]
        # domain of colors neighbors of nodes are colored in
        self.neighbors_constraints = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]
        # backjump stack
        self.backjump_stack = []

    # finds minimum remaining values variable with Highest Degree
    def MRVandHD(self):
        # calculates number of colors available for each node
        remaining_values = [0 for _ in range(self.graph.V+1)]
        for node in self.graph.uncolored_nodes:
            for color in range(self.graph.k):
                if self.my_domains[node.number][color] and not self.neighbors_constraints[node.number][color]:
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

    # check for node if exists a color, if so color the node
    def try_to_color(self, node):
        # update conflict sets
        node_time = self.coloring_time[node.number]
        for neigh in node.neighbors:
            neighbor_time = self.coloring_time[neigh.number]
            if neigh.color is not None and neighbor_time < node_time:
                self.conflict_set[node.number][neigh.number] = neighbor_time

        # colors used in past by "node", and colors of "node"s neighbors
        try_colors = self.get_colors_by_LCV(node)
        node_domain = self.my_domains[node.number]

        # iterating through nodes colors, if node didn't use color in past and neighbors not using color
        # than color is legal
        while not all(x == -1 for x in try_colors):
            # found legal color
            color = np.argmax(try_colors)
            try_colors[color] = -1
            node_domain[color] = False

            self.color_node(node, color)
            return True
        return False

    # color "node" with "color"
    def color_node(self, node, color):
        # use graphs coloring function
        self.graph.color_node(node, color)

        self.coloring_time[node.number] = self.conflict_counter
        self.conflict_counter += 1

        # update neighbor constraints based on coloring
        for neigh in node.neighbors:
            self.neighbors_constraints[neigh.number][color] += 1

    # uncolor "node"
    def uncolor_node(self, node, color):
        # use graphs uncoloring function
        self.graph.uncolor_node(node)

        # update neighbor constraints
        for neighbor in node.neighbors:
            self.neighbors_constraints[neighbor.number][color] -= 1

    # backjump to position of no dead end
    def backjump(self, node):
        # choosing dead end node by conflict set
        last_conflict = np.argmax(self.conflict_set[node.number])
        # if node has no conflicts -> no legal coloring exists
        if last_conflict == 0:
            return False

        # update conflict set of current node and last conflicts nodes
        for i, conf in enumerate(self.conflict_set[node.number]):
            if conf and i != last_conflict:
                self.conflict_set[last_conflict][i] = conf
        self.conflict_set[node.number] = [0 for _ in range(self.graph.V+1)]

        # initialize current nodes domain
        self.my_domains[node.number] = [True for _ in range(self.graph.k)]

        # remove color from dead end node
        lc_color = self.graph.nodes[last_conflict].color
        self.uncolor_node(self.graph.nodes[last_conflict], lc_color)
        for conf_set in self.conflict_set:
            conf_set[last_conflict] = 0
        self.backjump_stack.append(last_conflict)
        return True

    # coloring search function
    def backtracking(self):
        while len(self.graph.uncolored_nodes) > 1:
            print(len(self.graph.uncolored_nodes))
            next_node = self.MRVandHD() if not self.backjump_stack else self.graph.nodes[self.backjump_stack[-1]]
            if not self.try_to_color(next_node):
                if not self.backjump(next_node):
                    return False
            elif self.backjump_stack:
                self.backjump_stack.pop()
        return True

    # after finding a solution, try to improve upon it by removing largest color from domain
    def try_to_improve(self):
        self.graph.reset_new_k(self.graph.colors_used_until_now-1)
        self.conflict_counter = 1
        self.coloring_time = [np.inf for _ in range(self.graph.V+1)]
        self.conflict_set = [[0 for _ in range(self.graph.V+1)] for _ in range(self.graph.V+1)]
        self.my_domains = [[True for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]
        self.neighbors_constraints = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]