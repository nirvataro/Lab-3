from CSPcoloringHeuristics import MRV, LCV
import numpy as np
import sys
sys.setrecursionlimit(10000)


def backjumping(G, node):
    bad_node = np.argmax(G.nodes[node].conflict_set)
    for i, conf in enumerate(G.nodes[node].conflict_set):
        if conf and i != bad_node:
            G.nodes[bad_node].conflict_set[i] = conf
    change_node = np.argmax(G.nodes[bad_node].conflict_set)
    if change_node == 0:
        new_node_color = G.nodes[bad_node].possible_colors.index(0)
        G.uncolor_node(bad_node)
        G.color_node(bad_node, new_node_color)
        return
    G.uncolor_node(bad_node)
    while 0 not in G.nodes[change_node].possible_colors:
        G.uncolor_node(change_node)
        backjumping(G, change_node)
    change_node_color = G.nodes[change_node].possible_colors.index(0)
    G.uncolor_node(change_node)
    G.color_node(change_node, change_node_color)
    G.nodes[node].conflict_set = [0 for _ in G.nodes[node].conflict_set]
    return G


def backtracking(G):
    if not G.uncolored_nodes:
        return G
    nodes_by_MRV = MRV(G)
    for node in nodes_by_MRV:
        colors_to_check = node.domain.copy()
        colors_to_check = LCV(G, node, colors_to_check)
        if not colors_to_check:
            backjumping(G, node.number)
        else:
            G.color_node(node.number, colors_to_check[0])
    return backtracking(G)

