import main_local_search
import os
import sys

directory = 'data'
test = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        test.append(f)


for file in test:
    with open(file) as f:
        lines = f.readlines()
    for l in lines:
        l.strip()
    for idx, l in enumerate(lines):
        if l.startswith('p edge '):
            l = l.replace('p edge ', '').split()
            print(file, "\n", l[0])


