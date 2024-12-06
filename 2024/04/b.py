#!/usr/bin/env python

def reverse(lines):
    revlines = []

    for line in lines:
        revlines.append(line[::-1])

    return revlines


def flatten(flattenlist):
    return [x for xs in flattenlist for x in xs]


def a_coords_byrow(rowid, linetext):
    return [
        (rowid, i + 1) for i in range(
            len(linetext)
        ) if linetext.startswith('MAS', i)
    ]


def get_horizontal_a_locs(matrix):
    locs = []

    for rowid, line in enumerate(matrix):
        linetext = ''.join(line)
        locs.append(a_coords_byrow(rowid, linetext))
    for rowid, line in enumerate(matrix):
        linetext = ''.join(reverse(line))
        locs.append(a_coords_byrow(rowid, linetext))

    return flatten(locs)


def a_coords_bycol(colid, linetext):
    return [
        (i + 1, colid) for i in range(
            len(linetext)
        ) if linetext.startswith('MAS', i)
    ]


def get_vertical_a_locs(matrix):
    locs = []

    for colid in range(len(matrix[0])):
        linetext = ''.join([line[colid] for line in matrix])
        locs.append(a_coords_bycol(colid, linetext))
    for colid in range(len(matrix[0])):
        linetext = ''.join(reverse([line[colid] for line in matrix]))
        locs.append(a_coords_bycol(colid, linetext))

    return flatten(locs)


def get_diagonal_a_locs(matrix):
    locs = []

    for startcol in range(len(matrix[0])):
        newline = ""
        for iteration, row_id in enumerate(range(len(matrix) - startcol)):
            newline = newline + matrix[row_id][startcol+iteration]

        for pos in range(len(newline)):
            if newline.startswith('MAS', pos):
                locs.append((pos+1, startcol+pos+1))

    for iteration, startcol in enumerate(range(len(matrix[0]) - 1, -1, -1)):
        newline = ""
        for iteration, row_id in enumerate(range(len(matrix) - iteration)):
            newline = newline + matrix[row_id][startcol-iteration]

        for pos in range(len(newline)):
            if newline.startswith('MAS', pos):
                locs.append((pos+1, startcol-pos-1))

    for startrow in range(1, len(matrix)):
        newline = ""
        for iteration, col_id in enumerate(range(len(matrix) - startrow)):
            newline = newline + matrix[startrow+iteration][col_id]

        for pos in range(len(newline)):
            if newline.startswith('MAS', pos):
                locs.append((startrow+pos+1, pos+1))

    for startrow in range(1, len(matrix)):
        newline = ""
        for iteration, col_id in enumerate(range(len(matrix) - 1, startrow-1, -1)):
            newline = newline + matrix[startrow+iteration][col_id]

        for pos in range(len(newline)):
            if newline.startswith('MAS', pos):
                locs.append((startrow+pos+1, len(matrix[0])-pos+1-startrow))

    return locs


def create_loclist(matrix):
    horizontal_locs = get_horizontal_a_locs(matrix)
    vertical_locs = get_vertical_a_locs(matrix)
    diagonal_locs = get_diagonal_a_locs(matrix)

    print(len(horizontal_locs))
    print(len(vertical_locs))
    print(len(diagonal_locs))

    return horizontal_locs + vertical_locs + diagonal_locs


def main():
    matrix = []

    with open('input', 'r') as f:
        for line in f.readlines():
            matrix.append([char for char in line.strip()])

    searchlines = create_loclist(matrix)

    print(searchlines)
    print(len(set([i for i in searchlines if searchlines.count(i) > 1])))


if __name__ == '__main__':
    main()
