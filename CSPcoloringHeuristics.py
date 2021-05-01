
def MRV(graph):
    node = [graph.uncolored_nodes[0]]
    for v in graph.uncolored_nodes:
        if v.possible_colors < node[0].possible_colors:
            node = [v]
        elif v.possible_colors == node[0].possible_colors:
            node.append(v)

    return node[0] if len(node) == 1 else HD(graph, node)


def HD(graph, node_list):
    node = graph.nodes[node_list[0]]
    for v in node_list:
        if len(graph.nodes[v].possible_colors) < len(node.possible_colors):
            node = graph.nodes[v]
    return node


def LCV(graph, node):
    color = graph.least_constraining(node)
    graph.color_node(node, color)