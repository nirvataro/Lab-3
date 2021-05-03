# minimum remaining values
def MRV(graph):
    uncolored = [graph.nodes[i] for i in graph.uncolored_nodes]
    uncolored.sort(key=lambda x: len(x.domain))
    return HD(uncolored)


# highest degree
def HD(node_list):
    changed = True
    while changed:
        changed = False
        for i in range(len(node_list)-1):
            if len(node_list[i].domain) == len(node_list[i+1].domain):
                uncolored_i_neighbors = len(node_list[i].neighbors) - sum(node_list[i].possible_colors)
                uncolored_iplus1_neighbors = len(node_list[i+1].neighbors) - sum(node_list[i+1].possible_colors)
                if uncolored_i_neighbors < uncolored_iplus1_neighbors:
                    node_list[i], node_list[i+1] = node_list[i+1], node_list[i]
                    changed = True
    return node_list


def LCV(graph, node, colors):
    constraints = [[0, c] for i, c in enumerate(colors)]
    neighbors = [graph.nodes[neighbor] for neighbor in node.neighbors]
    for i, c in enumerate(colors):
        for neighbor in neighbors:
            constraints[i][0] += int(c in neighbor.domain)
    constraints.sort(key=lambda x: x[1])
    return [constraints[i][1] for i in range(len(constraints)) if constraints[i][0]]