import sys
from graphClass import Graph
from Feasible_local_search import FeasibleLocalSearch
from ForwardChecking import ForwardChecking
from Backtracking import BacktrackingWithBackjumping
from HybridLocalSearch import HybridLocalSearch as HLS
from Objective_local_search import ObjectiveLocalSearch as OLS
from SimulatedAnnealing import SimulatedAnnealing as SA
from GeneticAlgorithm import GeneticAlgorithm as GA
sys.setrecursionlimit(10000)


def CSP_coloring(graph):
    f_search = GA(graph)

    f_search.genetic()

    # while True:
    #     print(f_search.nodes_with_color)
    #     f_search = SA(f_search, search_time=120, output=True).saBest
    #     f_search.graph.draw()
    #     print(f_search.nodes_with_color)
    #     print(f_search.fitness)
    #     print("found")


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


    # search = ForwardChecking(graph)
    # while search.forward_checking():
    #     best_found = search.graph.__deepcopy__()
    #     best_found.draw()
    #     search.try_to_improve()
    # print("could not find better")