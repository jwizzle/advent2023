#!/usr/bin/env python3
import copy

GALAXY_STR = '#'
EMTPY_STR = '.'

class Galaxy():

    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col

    def get_shortest_path(self, other):
        shortrow = abs(self.row - other.row)
        shortcol = abs(self.col - other.col)

        return shortrow + shortcol

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return self.id

class Image():
    
    def __init__(self):
        self.matrix = []
        self.galaxies = []
        self.galaxy_pairs = []

    def expand(self):
        newmatrix = copy.deepcopy(self.matrix)
        space = 1000000-1

        rows_inserted = 0
        for id, row in enumerate(self.matrix):
            if not GALAXY_STR in row:
                empty_row = ['.']*len(row)
                blankspace = [empty_row]*space
                newmatrix = newmatrix[:id+rows_inserted] + blankspace + newmatrix[id+rows_inserted:]
                rows_inserted += space

        cols_inserted = 0
        for id, col in enumerate(self.matrix[0]):
            whole_col = [row[id] for row in self.matrix]
            if not GALAXY_STR in whole_col:
                for row_id, row in enumerate(newmatrix):
                    newmatrix[row_id] = newmatrix[row_id][:id + cols_inserted] + [EMTPY_STR]*space + newmatrix[row_id][id+cols_inserted:]
                cols_inserted += space

        return newmatrix

    def number_galaxies(self):
        galaxies = 1

        for row_id, row in enumerate(self.matrix):
            for col_id, col in enumerate(row):
                if col == GALAXY_STR:
                    newgalaxy = Galaxy(galaxies, row_id, col_id)
                    self.matrix[row_id][col_id] = newgalaxy
                    self.galaxies.append(newgalaxy)
                    galaxies += 1

    def fill_galaxy_pairs(self):
        pairlist = []

        for galaxy in self.galaxies:
            for other_galaxy in self.galaxies:
                if galaxy != other_galaxy:
                    pairlist.append(tuple(sorted([galaxy, other_galaxy])))

        return list(set(pairlist))

    def shortest_path_sum(self):
        total = 0
        for origin, destination in self.galaxy_pairs:
            total += origin.get_shortest_path(destination)
        return total

    def __repr__(self):
        newstr = ''
        for row in self.matrix:
            for col in row:
                newstr += str(col)
            newstr += '\n'
        return newstr

def main():
    image = Image()

    with open('input', 'r') as f:
        for line in f.readlines():
            image.matrix.append(list(line.strip()))

    image.matrix = image.expand()
    image.number_galaxies()
    image.galaxy_pairs = image.fill_galaxy_pairs()
    print(image.shortest_path_sum())

if __name__ == '__main__':
    main()
