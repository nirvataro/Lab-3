import main
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
    graph = main.config_data(file)
    print(file + " backtracking:\n\n")
    main.CSP_coloring(graph, 0, 180)
    print("\n\n--------------------------------------\n\n")
    print(file + " forwardchecking:\n\n")
    main.CSP_coloring(graph, 1, 180)

sys.stdout.close()
