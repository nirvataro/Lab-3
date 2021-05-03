
class Node:
    def __init__(self, number):
        self.number = number
        self.color = None
        self.neighbors = []

    def copy(self):
        copy = Node(self.number)
        copy.color = self.color
        copy.neighbors = self.neighbors.copy()
        return copy

    def add_edge(self, neighbor):
        self.neighbors.append(neighbor)


class LocalSearchGraph:
    def __init__(self, V, k):
        self.V = V
        self.k = k
        self.nodes = [Node(i) for i in range(V+1)]
        self.colors = [i for i in range(k)]
        self.best_k = 0

    def add_edge(self, v1, v2):
        self.nodes[v1].add_edge(v2)
        self.nodes[v2].add_edge(v1)

    def color_node(self, node, color):
        node.color = color

    def violations(self):
        vio = 0
        for node in self.nodes:
            for neighbor in node.neighbors:
                if node.color == self.nodes[neighbor].color:
                    vio += 1
        return vio/2

    def initial_solution(self):
        for node in self.nodes:
            neighbors = [self.nodes[neighbor] for neighbor in node.neighbors]
            neighbors_colors = [neighbor.color for neighbor in neighbors]
            for color in self.colors:
                if color not in neighbors_colors:
                    self.color_node(node, color)
                    if color > self.best_k:
                        self.best_k = color
        return self.best_k

    def copy(self):
        copy = LocalSearchGraph(self.V, self.k)
        copy.nodes = [node.copy() for node in self.nodes]
        copy.colors = [i for i in range(self.k)]
        copy.best_k = self.best_k
        return copy


    def smaller_domain(self):
        self.k = self.best_k - 1
        self.best_k = 0
        for node in self.nodes:
            if node.color == self.k:
                node.color = None
        self.colors = self.colors[:self.k]

    def get_neighborhood(self):
        neighborhood = []
        for node in self.nodes:
            for color in self.colors:
                graph = self.copy()
                graph.color_node(node, color)
                neighborhood.append(graph)
        return neighborhood