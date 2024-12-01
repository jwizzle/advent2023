#!/usr/bin/env python3

def resolve_node(node, direction):
    left, right = network_dict[node]

    if direction == 'R':
        return right
    else:
        return left


def follow_path(steps=0, path_index=0):
    global startnodes

    while True:
        direction = firstline[path_index]
        # We convert to a set, then back to a list.
        # Sets strip all doubles, if two nodes end up at the same spot we stop calculating them.
        startnodes = list(set([resolve_node(node, direction) for node in startnodes]))
        finished_nodes = [node for node in startnodes if node[-1] == 'Z']

        if finished_nodes == startnodes:
            return steps+1
        else:
            if path_index >= len(firstline)-1:
                path_index = 0
            else:
                path_index += 1

            steps += 1

network_dict = {}

with open('input', 'r') as f:
    text = f.read()

firstline = text.split('\n')[0]

for line in text.split('\n')[2:]:
    if line:
        node = line.split('=')[0].strip()
        destinations = line.split('=')[1].strip(')').strip(' (').split(', ')
        network_dict[node] = (destinations[0], destinations[1])

startnodes = [node for node in network_dict if node[-1] == 'A']
print(follow_path())
