#!/usr/bin/env python

def reverse(lines):
    revlines = []

    for line in lines:
        revlines.append(line[::-1])

    return revlines


def create_horizontal_lines(matrix):
    lines = []

    for line in matrix:
        lines.append(''.join(line))

    return lines


def create_vertical_lines(matrix):
    lines = []

    for id in range(len(matrix[0])):
        lines.append(''.join([line[id] for line in matrix]))

    return lines


def create_diagonal_lines(matrix):
    lines = []

    for startcol in range(len(matrix[0])):
        newline = ""
        for iteration, row_id in enumerate(range(len(matrix) - startcol)):
            newline = newline + matrix[row_id][startcol+iteration]

        lines.append(newline)

    for iteration, startcol in enumerate(range(len(matrix[0]) - 1, -1, -1)):
        newline = ""
        for iteration, row_id in enumerate(range(len(matrix) - iteration)):
            newline = newline + matrix[row_id][startcol-iteration]

        lines.append(newline)

    for startrow in range(1, len(matrix)):
        newline = ""
        for iteration, col_id in enumerate(range(len(matrix) - startrow)):
            newline = newline + matrix[startrow+iteration][col_id]

        lines.append(newline)

    for startrow in range(1, len(matrix)):
        newline = ""
        for iteration, col_id in enumerate(range(len(matrix) - 1, startrow-1, -1)):
            newline = newline + matrix[startrow+iteration][col_id]

        lines.append(newline)

    return lines


def create_searchlines(matrix):
    horizontal_lines = create_horizontal_lines(matrix)
    reversed_horizontal = reverse(horizontal_lines)
    vertical_lines = create_vertical_lines(matrix)
    reversed_vertical = reverse(vertical_lines)
    diagonal_lines = create_diagonal_lines(matrix)
    reversed_diagonal = reverse(diagonal_lines)

    searchlines = [
        horizontal_lines,
        reversed_horizontal,
        vertical_lines,
        reversed_vertical,
        diagonal_lines,
        reversed_diagonal,
    ]

    return [x for xs in searchlines for x in xs]


def main():
    matrix = []

    with open('input', 'r') as f:
        for line in f.readlines():
            matrix.append([char for char in line.strip()])

    searchlines = create_searchlines(matrix)

    total = 0
    for line in searchlines:
        total = total + line.count('XMAS')

    print(total)


if __name__ == '__main__':
    main()
