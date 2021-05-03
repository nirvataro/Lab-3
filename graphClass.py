import numpy as np


class Node:
    def __init__(self, number, k, V):
        self.neighbors = []
        self.number = number
        self.color = None
        # if possible_colors[i] == 0 -> can color node in color i
        self.possible_colors = [0 for _ in range(k)]
        self.conflict_set = [0 for _ in range(V+1)]
        self.domain = [i for i in range(k)]

    def add_edge(self, v2):
        if v2 not in self.neighbors:
            self.neighbors.append(v2)

    def __str__(self):
        return "Node Number: " + str(self.number) + "\nNode Color: " + str(self.color)


class Graph:
    def __init__(self, V, E, k):
        # array of graph nodes
        self.nodes = [Node(i, k, V) for i in range(V+1)]
        # graph density
        self.density = V/E
        # array of indices of uncolored nodes
        self.uncolored_nodes = [i for i in range(1, V + 1)]
        # array of indices of colored nodes
        self.colored_nodes = []
        # current k best
        self.best_k = 0
        # best k found
        self.global_best_k = 0
        # array of colors in cell i will be the number of color i was used
        self.colors = [0 for _ in range(k)]
        # uses to keep track of conflicts entry time to conflict set
        self.conflict_counter = 1
        self.edges = []

    # adds an edge (v1, v2)
    def add_edge(self, v1, v2):
        self.nodes[v1].add_edge(v2)
        self.nodes[v2].add_edge(v1)
        self.edges.append((v1, v2))

    # colors "node" in "color", updates uncolored_nodes, colored_nodes, neighbors possible colors & conflict set
    def color_node(self, node, color):
        if self.nodes[node].color is None:
            self.uncolored_nodes.remove(node)
            self.colored_nodes.append(node)
            self.nodes[node].color = color
            self.nodes[node].possible_colors[color] = -1
            self.colors[color] += 1
            if self.colors[color] == 1:
                self.best_k += 1
            for v in self.nodes[node].neighbors:
                self.nodes[v].possible_colors[color] += 1
                if self.nodes[v].possible_colors[color] == 1:
                    self.nodes[v].domain.remove(color)
                self.nodes[v].conflict_set[node] = self.conflict_counter
            self.conflict_counter += 1
            if not self.uncolored_nodes:
                self.global_best_k = self.best_k

    # uncolors "node", undoing same as "color_node"
    def uncolor_node(self, node):
        if self.nodes[node].color is not None:
            self.colored_nodes.remove(node)
            self.uncolored_nodes.append(node)
            old_color = self.nodes[node].color
            self.colors[old_color] -= 1
            self.nodes[node].possible_colors[old_color] = 0
            self.nodes[node].color = None
            if not self.colors[old_color]:
                self.best_k -= 1
            for v in self.nodes[node].neighbors:
                self.nodes[v].possible_colors[old_color] -= 1
                self.nodes[v].conflict_set[node] = 0
                if self.nodes[v].possible_colors[old_color] == 0:
                    self.nodes[v].domain.append(old_color)

    # returns a color for "node" that will least constrain its neighbor
    def least_constraining(self, node):
        neighbors = self.nodes[node].neighbors
        best_color, constraints, best_constraint = None, 0, 0
        for color, neighbors_with_color in enumerate(self.nodes[node].possible_colors):
            if not neighbors_with_color:
                for neigh in neighbors:
                    if not self.nodes[neigh].possible_colors[color]:
                        constraints += 1
                if best_color is None or constraints < best_constraint:
                    best_color = color
                    best_constraint = constraints
        return best_color

    # after finding a solution with k colors, try finding with k-1 colors
    def find_better(self):
        k = self.best_k
        for node in self.nodes:
            self.uncolor_node(node.number)
        for node in self.nodes:
            node.domain = [i for i in range(k-1)]
            node.possible_colors = node.possible_colors[:k - 1]
        self.colors = self.colors[:k-1]
        self.conflict_counter = 1

    def __str__(self):
        return "BEST K: " + str(self.global_best_k) + "\nMax K = " + str(len(self.colors))
