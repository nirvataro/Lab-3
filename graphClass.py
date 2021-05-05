import copy


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
        return "Node Number: " + str(self.number) + "\nNode Color: " + str(self.color)

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

    # adds an edge (v1, v2)
    def add_edge(self, v1, v2):
        self.nodes[v1].add_edge(self.nodes[v2])
        self.nodes[v2].add_edge(self.nodes[v1])

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
                    del self.uncolored_nodes[i]
                    break
            self.uncolored_nodes.append(v_copy)
            old_color = node.color
            self.times_used_color[old_color] -= 1
            node.color = None
            if self.times_used_color[old_color] == 0:
                self.colors_used_until_now -= 1

    # how I print a graph
    def __str__(self):
        output = "Best Solution Found:\nNumber of colors: " + str(self.colors_used_until_now) + "\nNode Coloring:\n"
        output += "Number\tColor\n"
        for node in self.nodes:
            output += str(node.number) + "\t" + str(node.color)
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
        return new

    # def initial_solution(self):
    #     for node in self.nodes:
    #         if not node.number:
    #             continue
    #         neighbors = [self.nodes[neighbor] for neighbor in node.neighbors]
    #         neighbors_colors = [neighbor.color for neighbor in neighbors]
    #         for color in range(len(self.colors)):
    #             if color not in neighbors_colors:
    #                 self.color_node(node.number, color)
    #                 continue
    #     return self.best_k

    # after finding a solution with k colors, try finding with k-1 colors
    # def find_better(self):
    #     k = self.best_k
    #     for node in self.nodes:
    #         self.uncolor_node(node.number)
    #     for node in self.nodes:
    #         node.domain = [i for i in range(k-1)]
    #         node.possible_colors = node.possible_colors[:k - 1]
    #     self.colors = self.colors[:k-1]
    #     self.conflict_counter = 1

    # def smaller_domain(self):
    #     k = self.best_k
    #     for node in self.nodes:
    #         if node.color == (k-1):
    #             self.uncolor_node(node.number)
    #         if (k-1) in node.domain:
    #             node.domain.remove(k-1)
    #         node.possible_colors = node.possible_colors[:k-1]
    #     self.colors = self.colors[:k-1]


