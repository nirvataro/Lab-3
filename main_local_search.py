import sys
import time
from graphClass import Graph
from HybridLocalSearch import HybridLocalSearch as HLS
from Objective_local_search import ObjectiveLocalSearch as OLS
from Feasible_local_search import FeasibleLocalSearch as FLS
from GeneticAlgorithm import GeneticAlgorithm as GA
from SimulatedAnnealing import SimulatedAnnealing as SA
sys.setrecursionlimit(10000)


algorithmDictionary = {0: HLS, 1: OLS, 2: FLS, 3: GA}
printDictionary = {0: "Hybrid Approach", 1: "Objective Function Approach", 2: "Feasible Approach", 3: "Genetic Algorithm"}


def CSP_coloring(graph, algorithm, search_time):
    print("Algorithm: ", printDictionary[algorithm])
    print("Search Time Limit: {} seconds".format(search_time))
    print(graph)
    print("Looking for initial solution")
    algorithm = algorithmDictionary[algorithm]
    local_search_graph = algorithm(graph, uncolored=True)
    sa_object = SA(local_search_graph)
    sa_object.sa_search(search_time=search_time, output=True)

    print("---------------TIMED OUT---------------\n")
    print("Best solution found for K={}\nTotal states: {}\n".format(sa_object.saBest.graph.colors_used_until_now, sa_object.iterations))
    show_graph = input("Do you want to see the graph coloring? Y/N\n")
    if show_graph in ['y', 'Y']:
        sa_object.saBest.graph.draw()


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

