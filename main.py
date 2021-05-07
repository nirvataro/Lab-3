import sys
from graphClass import Graph
from ForwardChecking import ForwardChecking
from Backtracking import BacktrackingWithBackjumping
from Objective_local_search import objective_local_search
from SimulatedAnnealing import SimulatedAnnealing as SA
sys.setrecursionlimit(10000)


def CSP_coloring(graph):
    search = BacktrackingWithBackjumping(graph)
    while search.backtracking():
        best_found = search.graph.__deepcopy__()
        best_found.draw()
        search.try_to_improve()
    print("could not find better")


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
    graph.preprocessing()
    return graph


if __name__ == '__main__':
    input_file = sys.argv[1]
    graph = config_data(input_file)
    CSP_coloring(graph)
