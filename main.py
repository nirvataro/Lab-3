from sys import argv
import sys
from graphClass import Graph
from ForwardChecking import forward_checking
from Backtracking import BacktrackingWithBackjumping
from Objective_local_search import objective_local_search
from SimulatedAnnealing import SimulatedAnnealing as SA
sys.setrecursionlimit(10000)

def CSP_coloring(graph):
    back_jump = BacktrackingWithBackjumping(graph)
    while True:
        if back_jump.backtracking():
            best_found = back_jump.graph.__deepcopy__()
            print(back_jump.graph)
            for node in back_jump.graph.nodes:
                for neigh in node.neighbors:
                    if node.color == neigh.color:
                        print(node, neigh)
        back_jump.try_to_improve()



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
