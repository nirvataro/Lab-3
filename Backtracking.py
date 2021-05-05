from CSPcoloringHeuristics import MRV, LCV
import numpy as np
import sys
sys.setrecursionlimit(10000)


class BacktrackingWithBackjumping():
    def __init__(self, graph):
        self.graph = graph.__deepcopy__()
        self.conflict_set = [[0 for _ in range(self.graph.V)]*self.graph.V]
        # uses to keep track of conflicts entry time to conflict set
        self.conflict_counter = 1
        self.domains = [[1 for _ in range(len(self.graph.colors))]*self.graph.V]

    def try_to_color(self, node_number):
        node_domain = self.domains[node_number]
        if not sum(node_domain):
            return False
        node_neighbors_colors = [self.graph.nodes[neigh].color for neigh in self.graph.nodes[node_number].neigbors]
        for i in range(len(node_domain)):
            if node_domain[i] and i not in node_neighbors_colors:
                node_domain[i] = 0
                return i
        return False


    def color_node(self, node_number, color):
        self.graph.color_node(node_number, color)

        for neigh in self.graph.nodes[node_number].neighbors:
            self.conflict_set[neigh][node_number] = self.conflict_counter
        self.conflict_counter += 1

    def uncolor_node(self, node_number):
        self.graph.uncolor_node(node_number)

        for neigh in self.graph.nodes[node_number].neighbors:
            self.conflict_set[neigh][node_number] = 0

    def backjumping(self, node):
        last_conflict = np.argmax(self.conflict_set[node])
        for i, conf in enumerate(self.conflict_set[node]):
            if conf and i != last_conflict:
                self.conflict_set[last_conflict][i] = conf

        self.uncolor_node(last_conflict)

        # for color in self.graph.nodes[last_conflict].domain:
        #
        # hile 0 not in G.nodes[change_node].possible_colors:
        #     G.uncolor_node(change_node)
        #     backjumping(G, change_node)
        # change_node_color = G.nodes[change_node].possible_colors.index(0)
        # G.uncolor_node(change_node)
        # G.color_node(change_node, change_node_color)
        # G.nodes[node].conflict_set = [0 for _ in G.nodes[node].conflict_set]
        # return G

    def backtracking(self, G):
        if not G.uncolored_nodes:
            return G
        nodes_by_MRV = MRV(G)
        for node in nodes_by_MRV:
            colors_to_check = node.domain.copy()
            colors_to_check = LCV(G, node, colors_to_check)
            if not colors_to_check:
                self.backjumping(G, node.number)
            else:
                G.color_node(node.number, colors_to_check[0])
        return self.backtracking(G)

