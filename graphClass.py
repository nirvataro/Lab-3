class Node:
    def __init__(self, number):
        self.neighbors = []
        self.number = number
        self.color = None
        self.possible_colors = []

    def add_edge(self, v2):
        if v2 not in self.neighbors:
            self.neighbors.append(v2)


class Graph:
    def __init__(self, V):
        self.nodes = [Node(i) for i in range(V+1)]
        self.uncolored_nodes = [i for i in range(1, V+1)]
        self.colored_nodes = []
        self.edges = []
        self.colors = 0

    def add_edge(self, v1, v2):
        self.nodes[v1].add_edge(v2)
        self.nodes[v2].add_edge(v1)
        self.edges.append((v1, v2))

    def color_node(self, node, color):
        self.uncolored_nodes.remove(node)
        self.colored_nodes.append(node)
        self.nodes[node].color = color
        for v in self.nodes[node].neighbors:
            self.nodes[v].possible_colors.remove(color)

    def uncolor_node(self, node):
        self.colored_nodes.remove(node)
        self.uncolored_nodes.append(node)
        old_color = self.nodes[node].color
        self.nodes[node].color = None
        for v in self.nodes[node].neighbors:
            self.nodes[v].possible_colors.append(old_color)

    def least_constraining(self, node):
        colors = self.nodes[node].possible_colors
        best_color = None
        best = 0
        for c in colors:
            possibilities = 0
            for neigh in self.nodes[node].neighbors:
                if neigh in self.uncolored_nodes:
                    possibilities += sum(1 for n in self.nodes[neigh].possible_colors if n != c)
            if possibilities > best:
                best_color = c
        return best_color
