from LocalSeachGraph import LocalSearchGraph
import random
import SimulatedAnnealing as SA


def feasable_local_search(graph):
    # find initial solution
    k = graph.initial_solution()

    # remove 1 color
    graph.smaller_domain()
    for node in graph.nodes:
        if node.color is None:
            graph.color_node(node, random.choice(list(range(k-1))))

