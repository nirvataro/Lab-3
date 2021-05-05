from CSPcoloringHeuristics import MRV, LCV
import numpy as np
import sys
sys.setrecursionlimit(10000)


class BacktrackingWithBackjumping():
    def __init__(self, graph):
        self.graph = graph.__deepcopy__()
        # uses to keep track of conflicts entry time to conflict set
        self.conflict_counter = 1
        self.conflict_set = [[0 for _ in range(self.graph.V)] * self.graph.V]
        self.my_domains = [[True for _ in range(len(self.graph.colors))]*self.graph.V]
        self.neighbors_constraints = [[0 for _ in range(len(self.graph.colors))]*self.graph.V]

    def try_to_color(self, node_number):
        node_domain = self.domains[node_number]
        if not sum(node_domain):
            return False
        node_neighbors_colors = [self.graph.nodes[neigh].color for neigh in self.graph.nodes[node_number].neigbors]
        for i in range(len(node_domain)):
            if node_domain[i] and i not in node_neighbors_colors:
                node_domain[i] = 0
                return i
        return None

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
            next_node_number = self.MRV()
            color = self.try_to_color(next_node_number)
            if color is None:
                self.backjump(next_node_number)
        return True

