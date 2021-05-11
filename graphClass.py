import random
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, number, color=None):
        self.neighbors = []
        self.number = number
        self.color = color

    # adds neighbor "node" object as neighbor
    def add_edge(self, v2):
        if v2 not in self.neighbors:
            self.neighbors.append(v2)

    def __str__(self):
        return "Node Number: " + str(self.number) + "\nNode Color: " + str(self.color) + "\n"

    def __deepcopy__(self):
        new = Node(self.number, self.color)
        return new


class Graph:
    def __init__(self, V, E, k=None, copy=False):
        if k is None:
            k = V
        # number of vertices, edges, colors, graph density
        self.V = V
        self.E = E
        self.k = k
        self.density = V / E
        if not copy:
            # array of graph nodes
            self.nodes = [Node(i) for i in range(V+1)]
            # array of indices of uncolored nodes
            self.uncolored_nodes = [self.nodes[node.number] for node in self.nodes]
            # array of colors in cell i will be the number of color i was used
            self.times_used_color = [0 for _ in range(k)]
        else:
            self.nodes = []
            self.uncolored_nodes = []
            self.times_used_color =[]

        # array of indices of colored nodes
        self.colored_nodes = []
        # current k best
        self.colors_used_until_now = 0
        self.edges = []

    # how I print a graph
    def __str__(self):
        output = "Graph details:\n\tNumber of vertices: " + str(self.V) + "\n\tNumber of edges: " + str(self.E) + "\n\tGraph density: " + str(self.density) + "\n"
        return output

    # copy graph method
    def __deepcopy__(self):
        new = Graph(self.V, self.E, self.k, copy=True)
        new.nodes = [node.__deepcopy__() for node in self.nodes]
        for v1 in new.nodes:
            for v2 in self.nodes[v1.number].neighbors:
                v1.add_edge(new.nodes[v2.number])
        new.uncolored_nodes = [new.nodes[node.number] for node in self.uncolored_nodes]
        new.colored_nodes = [new.nodes[node.number] for node in self.colored_nodes]
        new.colors_used_until_now = self.colors_used_until_now
        new.times_used_color = self.times_used_color.copy()
        new.edges = self.edges.copy()
        return new

    # adds an edge (v1, v2)
    def add_edge(self, v1, v2):
        self.nodes[v1].add_edge(self.nodes[v2])
        self.nodes[v2].add_edge(self.nodes[v1])
        self.edges.append((v1, v2))

    # colors "node" in "color", updates uncolored_nodes and colored_nodes
    def color_node(self, node, color):
        if node.color is None:
            for i, v in enumerate(self.uncolored_nodes):
                if v.number == node.number:
                    v_copy = v
                    del self.uncolored_nodes[i]
                    break
            self.colored_nodes.append(v_copy)
            node.color = color
            self.times_used_color[color] += 1
            if self.times_used_color[color] == 1:
                self.colors_used_until_now += 1
            if not self.uncolored_nodes:
                self.k = self.colors_used_until_now

    # uncolors "node", updates uncolored and colored nodes
    def uncolor_node(self, node):
        if node.color is not None:
            for i, v in enumerate(self.colored_nodes):
                if v.number == node.number:
                    v_copy = v
                    del self.colored_nodes[i]
                    break
            self.uncolored_nodes.append(v_copy)
            old_color = node.color
            self.times_used_color[old_color] -= 1
            node.color = None
            if self.times_used_color[old_color] == 0:
                self.colors_used_until_now -= 1

    def reset_new_k(self, k=None):
        if k is None:
            self.k = self.colors_used_until_now - 1
        else:
            self.k = k
        for node in self.nodes:
            self.uncolor_node(node)

    def preprocessing(self):
        # upper bound of coloring is max degree+1
        max_degree = 0
        for node in self.nodes:
            if len(node.neighbors) > max_degree:
                max_degree = len(node.neighbors)
        self.k = max_degree + 1

    # drawing the graph
    def draw(self, nodes=None, neighbors_node=None):
        if nodes is None:
            nodes = list(range(1, self.V+1))

        nodes = set(nodes)
        if neighbors_node is not None:
            for node in neighbors_node:
                for neigh in self.nodes[node].neighbors:
                    nodes.add(neigh.number)

        G = nx.Graph()
        G.add_nodes_from(nodes)
        edges = []
        for v1, v2 in self.edges:
            if v1 in nodes and v2 in nodes:
                edges.append((v1, v2))
        G.add_edges_from(edges)
        node_color = ["#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(self.k)]

        color_map = []
        for node in nodes:
            color_map.append(node_color[self.nodes[node].color])
        nx.draw(G, node_color=color_map, with_labels=True)
        text = "Number of nodes: " + str(self.V) + "\nNumber of edges: " + str(self.E) + "\nDensity: " + \
               str(self.density) + "\nNumber of colors: " + str(self.colors_used_until_now)

        plt.figtext(0.5, 0.01, text, ha="left", va='bottom', fontsize=16,
                   bbox={"facecolor": "cyan", "alpha": 0.5, "pad": 5})
        plt.show()
