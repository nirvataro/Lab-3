def MRV(graph):
    node = [graph.uncolored_nodes[0]]
    for v in graph.uncolored_nodes:
        colors = len([0 for i in graph.nodes[v].possible_colors if not i])
        node_colors = len([0 for i in graph.nodes[node[0]].possible_colors if not i])
        if colors < node_colors:
            node = [v]
        elif colors == node_colors and v not in node:
            node.append(v)
    return node[0] if len(node) == 1 else HD(graph, node)


def HD(graph, node_list):
    node = graph.nodes[node_list[0]]
    for v in node_list:
        if len(graph.nodes[v].possible_colors) < len(node.possible_colors):
            node = graph.nodes[v]
    return node.number


def LCV(graph, node):
    color = graph.least_constraining(node)
    if color is None:
        return None
    graph.color_node(node, color)
    return True
