import sys
from graphClass import Graph
from GeneticAlgorithm import GeneticAlgorithm as GA


def CSP_coloring(graph, search_time):
    print("Genetic Algorithm with Hybrid Approach")
    print("Search Time Limit: {} seconds".format(search_time))
    print(graph)
    print("Looking for initial solution")
    genetic_object = GA(graph)
    genetic_object.genetic(search_time=search_time)

    print("---------------TIMED OUT---------------\n")
    print("Best solution found for K={}\nTotal states: {}\n".format(genetic_object.gen_arr[0].graph.colors_used_until_now, genetic_object.iterations))
    show_graph = input("Do you want to see the graph coloring? Y/N\n")
    if show_graph in ['y', 'Y']:
        genetic_object.gen_arr[0].graph.draw()


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
    time_limit = int(sys.argv[2])
    graph = config_data(input_file)
    CSP_coloring(graph, time_limit)
