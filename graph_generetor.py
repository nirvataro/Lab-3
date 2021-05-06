import random
from sys import argv


def main():
    file = "ex_30.txt"
    nodes_number = 30
    file = open(file, "w+")
    text = ""

    count = 0
    for i in range(1, nodes_number+1):
        for j in range(i+1, nodes_number+1):
            if random.random() < 0.2:
                text += "e " + str(i) + " " + str(j) + '\n'
                count += 1

    file.write("p edge " + str(nodes_number) + " " + str(count) + '\n' + text)
    file.close()


if __name__ == '__main__':
    main()
