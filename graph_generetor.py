import random
from sys import argv


def main():
    file = "ex_5.txt"
    nodes_number = 5
    edge_prob = 0.2
    file = open(file, "w+")
    text = ""

    count = 0
    for i in range(1, nodes_number+1):
        for j in range(i+1, nodes_number+1):
            if random.random() < edge_prob:
                text += "e " + str(i) + " " + str(j) + '\n'
                count += 1

    file.write("p edge " + str(nodes_number) + " " + str(count) + '\n' + text)
    file.close()


if __name__ == '__main__':
    main()
