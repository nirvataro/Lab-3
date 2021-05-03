from CSPcoloringHeuristics import MRV, LCV


def arc_consistency(G, node, colors):
    for c in colors:
        for neighbor in node.neighbors:
            if len(G.nodes[neighbor].domain) == 1 and (c in G.nodes[neighbor].domain):
                colors.remove(c)


def forward_checking(G):
    if not G.uncolored_nodes:
        return True
    nodes_by_MRV = MRV(G)
    for node in nodes_by_MRV:
        colors_to_check = node.domain.copy()
        arc_consistency(G, node, colors_to_check)
        colors_to_check = LCV(G, node, colors_to_check)
        if not colors_to_check:
            return False
        for color in colors_to_check:
            G.color_node(node.number, color)
            if not forward_checking(G):
                G.uncolor_node(node.number)
            else:
                return True
    return False
