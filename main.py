from sys import argv
from graphClass import Graph


def CSP_coloring(graph):
    return



def config_data(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    for l in lines:
        l.strip()
    for idx, l in enumerate(lines):
        if l.startswith('p edge '):
            l = l.replace('p edge ', '').split()
            graph = Graph(int(l[0]))
        elif l.startswith('e '):
            l = l.replace('e ', '').split()
            graph.add_edge(int(l[0]), int(l[1]))
    return graph


if __name__ == '__main__':
    input_file = argv[1]
    graph = config_data(input_file)
    CSP_coloring(graph)
