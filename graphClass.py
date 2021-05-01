import numpy as np


class Node:
    def __init__(self, number, k, V):
        self.neighbors = []
        self.number = number
        self.color = None
        self.possible_colors = [0 for _ in range(k)]
        self.conflict_set = [0 for _ in range(V+1)]

    def add_edge(self, v2):
        if v2 not in self.neighbors:
            self.neighbors.append(v2)


class Graph:
    def __init__(self, V, E, k):
        self.nodes = [Node(i, k, V) for i in range(V+1)]
        self.uncolored_nodes = [i for i in range(1, V+1)]
        self.density = V/E
        self.colored_nodes = []
        self.best_k = 0
        self.global_best_k = 0
        self.colors = [0 for _ in range(k)]
        self.conflict_counter = 1

    def add_edge(self, v1, v2):
        self.nodes[v1].add_edge(v2)
        self.nodes[v2].add_edge(v1)

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
                self.nodes[v].conflict_set[node] = self.conflict_counter
            self.conflict_counter += 1
            if not self.uncolored_nodes:
                self.global_best_k = self.best_k

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

    def least_constraining(self, node):
        if 0 not in self.nodes[node].possible_colors:
            return None
        colors = [0 for _ in range(len(self.nodes[node].possible_colors))]
        for neigh in self.nodes[node].neighbors:
            if neigh in self.uncolored_nodes:
                for c in range(len(colors)):
                    if not self.nodes[neigh].possible_colors[c]:
                        colors[c] += 1
        return np.argmax(colors)

    def find_better(self):
        k = self.best_k
        for node in self.nodes:
            if node.color == k-1:
                self.uncolor_node(node.number)
        for node in self.nodes:
            node.possible_colors = node.possible_colors[:k-1]
        self.colors = self.colors[:k - 1]

    def __str__(self):
        return "BEST K: " + str(self.global_best_k) + "\nMax K = " + str(len(self.colors))
