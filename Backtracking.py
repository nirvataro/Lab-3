from CSPcoloringHeuristics import MRV, LCV
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
        self.my_domains = [[True for _ in range(len(self.graph.colors))]*self.graph.V]
        # domain of colors neighbors of nodes are colored in
        self.neighbors_constraints = [[0 for _ in range(len(self.graph.colors))]*self.graph.V]

    # finds minimum remaining values variable with Highest Degree
    def MRVandHD(self):
        remaining_neighbor_colors = [sum([int(neigh[j]) for j in len(range(neigh))]) for neigh in self.neighbors_constraints]
        remaining_values = [int(self.my_domains[i]) + remaining_neighbor_colors[i] for i in range(len(self.neighbors_constraints))]
        min_remaining_values = min(remaining_values)
        nodes_min_remaining = [i for i in range(len(remaining_values)) if i == min_remaining_values]
        highest_degree = 0
        for node_number in nodes_min_remaining:
            if len(self.graph.nodes[node_number].neighbors) > highest_degree:
                best_node = self.graph.nodes[node_number]
                highest_degree = len(self.graph.nodes[node_number].neighbors)
        return best_node

    # check for node_number if exists a color, if so color the node
    def try_to_color(self, node_number):
        # colors used in past by "node", and colors of "node"s neighbors
        node_domain = self.my_domains[node_number]
        node_neighbor_constraint = self.neighbors_constraints[node_number]

        # iterating through nodes colors, if node didnt use color in past and neighbors not using color
        # than color is legal
        for color, untried, in_neighbors in enumerate(zip(node_domain, node_neighbor_constraint)):
            if untried and in_neighbors:
                # found legal color
                self.color_node(self.graph.nodes[node_number], color)
                node_domain[color] = False
                return True
        # unable to find color
        return False

    def color_node(self, node, color):
        self.graph.color_node(node, color)

        for neigh in node.neighbors:
            self.conflict_set[neigh.number][node.number] = self.conflict_counter
            self.neighbors_constraints[neigh.number][color] += 1
        self.conflict_counter += 1

    def uncolor_node(self, node, color):
        self.graph.uncolor_node(node)

        for neighbor in node.neighbors:
            self.neighbors_constraints[neighbor.number][color] -= 1

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

    def backtracking(self):
        while self.graph.uncolored_nodes:
            next_node_number = self.MRVandHD()
            if not self.try_to_color(next_node_number):
                if not self.backjump(next_node_number):
                    return False
        return True
