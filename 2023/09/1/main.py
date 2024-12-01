#!/usr/bin/env python3

def get_differences(sequence):
    """Return a new sequence of differences between steps."""
    differences = []
    loop_seq = sequence[1:]

    for id, num in enumerate(loop_seq):
        differences.append(num - sequence[id])

    return differences

def build_difference_list(sequence):
    """Builds a list of lists, containing differences until 0,0,0,0"""
    differences = [sequence]

    while list(set(differences[-1])) != [0]:
        differences.append(get_differences(differences[-1]))

    return differences

def extrapolate(difference_list):
    """Extrapolate from a list of lists containing differences until 0,0,0,0"""
    reverse_history = difference_list[::-1]
    added_value = 0

    for step in reverse_history:
        last_value = step[-1]
        added_value = added_value + last_value

    return added_value

def main():
    values = []

    with open('input', 'r') as f:
        for line in f.readlines():
            values.append([int(i) for i in line.strip().split(' ')])

    result = 0
    for sequence in values:
        difference_list = build_difference_list(sequence)
        result += extrapolate(difference_list)

    print(result)

if __name__ == '__main__':
    main()
