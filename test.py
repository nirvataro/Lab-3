import main_local_search
import os
import sys

directory = 'data'
test = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        test.append(f)

sys.stdout = open('output.txt', 'w')

for file in test:
    graph = main_local_search.config_data(file)
    print(file + " backtracking:\n\n")
    main_local_search.CSP_coloring(graph, 0, 180)
    print("\n\n--------------------------------------\n\n")
    print(file + " forwardchecking:\n\n")
    main_local_search.CSP_coloring(graph, 1, 180)

sys.stdout.close()
