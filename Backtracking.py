from CSPcoloringHeuristics import MRV, LCV
import numpy as np
import sys
sys.setrecursionlimit(10000)

heu = {'mrv': MRV, 'lcv': LCV}


def backjumping(G, node):
    bad_node = np.argmax(G.nodes[node].conflict_set)
    for i, conf in enumerate(G.nodes[node].conflict_set):
        if conf and i != bad_node:
            G.nodes[bad_node].conflict_set[i] = conf
    # G.nodes[node].conflict_set = [0 for _ in G.nodes[node].conflict_set]
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
    return G


def backtracking(G, heuristic):
    if not G.uncolored_nodes:
        return G
    next_node = MRV(G)
    colorable = LCV(G, next_node)
    # if 0 in G.nodes[next_node].possible_colors:
    #     next_node_color = G.nodes[next_node].possible_colors.index(0)
    #     G.color_node(next_node, next_node_color)
    # else:
    if not colorable:
        backjumping(G, next_node)
    return backtracking(G, heuristic)

