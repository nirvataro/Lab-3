import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    G = nx.DiGraph()
    G.add_edges_from(graph.edges)
    node_color = ['#003366', '#33cc33', '#ff0066', '#cc9900', '#cc33ff', '#00ccff', '#00ff00', '#ffcccc', '#9933ff', '#ff3300', '#4d0f00', '#737373', '#000000', '#ffff00', '#ffffcc', '#b35900', '#9900cc', '#f2ccff', '#cc0099', '#ff33cc', '#ff6666', '#1a53ff', '#99ffe6', '#00cccc']
    color_map = []
    for node in graph.nodes[1:]:
        color_map.append(node_color[node.color])
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()
