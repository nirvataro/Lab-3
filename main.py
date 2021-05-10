import sys
import time
from graphClass import Graph
from ForwardChecking import ForwardChecking as FC
from Backtracking import BacktrackingWithBackjumping as BB
from HybridLocalSearch import HybridLocalSearch as HLS
from Objective_local_search import ObjectiveLocalSearch as OLS
from Feasible_local_search import FeasibleLocalSearch as FLS
from SimulatedAnnealing import SimulatedAnnealing as SA
from GeneticAlgorithm import GeneticAlgorithm as GA
sys.setrecursionlimit(10000)


algorithmDictionary = {0: BB, 1: FC}


def CSP_coloring(graph, algorithm, search_time):
    algorithm = algorithmDictionary[algorithm]
    search = algorithm(graph)
    end_time = time.time() + search_time
    time_left = end_time - time.time()
    print("Looking for initial solution")
    while time_left > 0:
        if search.search(end_time):
            best_graph = search.graph.__deepcopy__()
            print("Solution found for K={}".format(best_graph.colors_used_until_now))
            print("Looking for solution for K={}".format(best_graph.colors_used_until_now-1))
        search.try_to_improve()
        time_left = end_time - time.time()

    print("---------------TIMED OUT---------------\n")
    print("Best solution found for K={}\nTotal states: {}\n".format(best_graph.colors_used_until_now, search.states))
    show_graph = input("Do you want to see the graph coloring? Y/N")
    if show_graph in ['y', 'Y']:
        best_graph.draw()


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
    algorithm = int(sys.argv[2])
    time_limit = int(sys.argv[3])
    graph = config_data(input_file)
    CSP_coloring(graph, algorithm, time_limit)

    # f_search = GA(graph)
    # f_search.genetic()
