from sys import argv
from graphClass import Graph
from ForwardChecking import forward_checking
from Backtracking import backtracking


def CSP_coloring(graph):
    while True:
        graph = backtracking(graph, 'mrv')
        print(graph)
        for node in graph.nodes:
            for neigh in node.neighbors:
                if node.color == graph.nodes[neigh].color:
                    print(node.number, neigh, node.color, graph.nodes[neigh].color)

        if not graph.uncolored_nodes:
            graph.find_better()


def config_data(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    for l in lines:
        l.strip()
    for idx, l in enumerate(lines):
        if l.startswith('p edge '):
            l = l.replace('p edge ', '').split()
            graph = Graph(int(l[0]), int(l[1]), int(l[0]))
        elif l.startswith('e '):
            l = l.replace('e ', '').split()
            graph.add_edge(int(l[0]), int(l[1]))
    return graph


if __name__ == '__main__':
    input_file = argv[1]
    graph = config_data(input_file)
    CSP_coloring(graph)
