from CSPcoloringHeuristics import MRV, LCV


def arc_consistency(G):
    pass


def forward_checking(G):
    arc_consistency(G)
    while G.uncolored_nodes:
        next_node = MRV(G)
        if 0 in G.nodes[next_node].possible_colors:
            next_node_color = G.nodes[next_node].possible_colors.index(0)
        else:

            G.color_node(next_node, next_node_color)
    return G