from CSPcoloringHeuristics import MRV, LCV


def arc_consistency(G, node, colors):
    for c in colors:
        for neighbor in G.nodes[node].neighbor:
            if len(G.nodes[neighbor].domain) == 1 and (c in G.nodes[neighbor].domain):
                colors.remove(c)


def forward_checking(G):
    if not G.uncolored_nodes:
        return True
    nodes_by_MRV = MRV(G) # fix so MRV returns sorted array
    for node in nodes_by_MRV:
        # add domain
        colors_to_check = G.nodes[node].domain.copy()
        arc_consistency(G, node, colors_to_check)
        LCV(G, colors_to_check) # fix so LCV returns array of colors sorted by constrains
        if not colors_to_check:
            return False
        for color in colors_to_check:
            G.color_node(node, color)
            if not forward_checking(G):
                G.uncolor_node(node)
            else:
                return True
    return False
