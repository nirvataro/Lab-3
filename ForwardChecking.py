from CSPcoloringHeuristics import MRV, LCV
import numpy as np
import sys
sys.setrecursionlimit(1000000)


class ForwardChecking:
    def __init__(self, graph):
        self.graph = graph.__deepcopy__()
        # domain of colors neighbors of nodes are colored in
        self.neighbors_constraints = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]

    # finds minimum remaining values variable with Highest Degree
    def MRVandHD(self):
        # calculates number of colors available for each node
        remaining_values = [available_colors.count(0) for available_colors in self.neighbors_constraints]
        remaining_values[0] = np.inf

        # sort the node based on minimum values available
        mrv_list = np.argsort(remaining_values).tolist()

        # find all nodes with minimum number of values available
        i = 0
        while i < len(mrv_list)-1:
            for j in range(i, len(mrv_list)):
                if not remaining_values[mrv_list[i]] == remaining_values[mrv_list[j]]:
                    equal_list = mrv_list[i:j]
                    equal_list.sort(key=lambda x: len(self.graph.nodes[x].neighbors), reverse=True)
                    mrv_list[i:j] = equal_list
                    i = j
                    break

        for node in self.graph.colored_nodes:
            if node.number in mrv_list:
                mrv_list.remove(node.number)

        for i, node in enumerate(mrv_list):
            mrv_list[i] = self.graph.nodes[node]

        return mrv_list

    # finds least constraining color for "node"
    def get_colors_by_LCV(self, node, colors):
        neighbors = node.neighbors
        color_constraints = [np.inf for _ in range(self.graph.k)]
        for i in range(self.graph.k):
            if i in colors:
                color_constraints[i] = 0

        for color in colors:
            for neigh in neighbors:
                if self.neighbors_constraints[neigh.number][color] != 0:
                    color_constraints[color] += 1

        colors.sort(key=(lambda x: color_constraints[x]))
        return colors

    # ------------------------------------------------------------------------ #
    # color "node" with "color"
    def color_node(self, node, color):
        # use graphs coloring function
        self.graph.color_node(node, color)

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
    # ------------------------------------------------------------------------ #

    def arc_consistency(self, node):
        my_domain = [i for i in range(self.graph.k) if self.neighbors_constraints[node.number][i] == 0]
        for color in my_domain:
            for neighbor in node.neighbors:
                indices = np.where(self.neighbors_constraints[neighbor.number] == 0)[0]
                if len(indices) == 1 and indices[0] == color:
                    my_domain.remove(color)
        return my_domain

    def forward_checking(self):
        if len(self.graph.uncolored_nodes) == 1:
            return True
        next_node_list = self.MRVandHD()
        for next_node in next_node_list:
            next_node_colors = self.arc_consistency(next_node)
            next_node_colors = self.get_colors_by_LCV(next_node, next_node_colors)
            if not next_node_colors:
                return False
            for color in next_node_colors:
                self.color_node(next_node, color)
                if not self.forward_checking():
                    self.uncolor_node(next_node, next_node.color)
                else:
                    return True
        return False

    # after finding a solution, try to improve upon it by removing largest color from domain
    def try_to_improve(self):
        self.graph.reset_new_k(self.graph.colors_used_until_now-1)
        self.neighbors_constraints = [[0 for _ in range(self.graph.k)] for _ in range(self.graph.V+1)]






 # def arc_consistency(self, G, node, colors):
 #        for c in colors:
 #            for neighbor in node.neighbors:
 #                if len(G.nodes[neighbor].domain) == 1 and (c in G.nodes[neighbor].domain):
 #                    colors.remove(c)
 #
 #    def forward_checking(self):
 #        if not self.graph.uncolored_nodes:
 #            return True
 #        nodes_by_MRV = self.MRVandHD()
 #        for node in nodes_by_MRV:
 #            colors_to_check = node.domain.copy()
 #            arc_consistency(G, node, colors_to_check)
 #            colors_to_check = LCV(G, node, colors_to_check)
 #            if not colors_to_check:
 #                return False
 #            for color in colors_to_check:
 #                G.color_node(node.number, color)
 #                if not forward_checking(G):
 #                    G.uncolor_node(node.number)
 #                else:
 #                    return True
 #        return False