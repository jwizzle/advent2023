#!/usr/bin/env python3

def follow_path(path, network_dict):
    currentnode = 'AAA'
    steps = 0

    while True:
        for c in path:
            left, right = network_dict[currentnode]
            if c == 'R':
                currentnode = right
            else:
                currentnode = left

            if currentnode == 'ZZZ':
                return steps + 1
            else:
                steps += 1

def main():
    firstline = ''
    network_dict = {}

    with open('input', 'r') as f:
        text = f.read()

    firstline = text.split('\n')[0]

    for line in text.split('\n')[2:]:
        if line:
            node = line.split('=')[0].strip()
            destinations = line.split('=')[1].strip(')').strip(' (').split(', ')
            network_dict[node] = (destinations[0], destinations[1])

    print(follow_path(firstline, network_dict))

if __name__ == '__main__':
    main()
