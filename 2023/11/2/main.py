#!/usr/bin/env python3
import copy
import numpy as np
import pandas as pd

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
        newmatrix = pd.DataFrame(data=self.matrix)
        space = 1000000

        for id in newmatrix.columns:
            if '#' not in newmatrix.iloc[:, id].unique():
                newcols = {col: col+space-1 for col in newmatrix.columns[id:]}
                newmatrix.rename(columns=newcols, inplace=True)

        for id in newmatrix.index:
            if '#' not in newmatrix.iloc[id, :].unique():
                newrows = {row: row+space-1 for row in newmatrix.index[id:]}
                newmatrix.rename(index=newrows, inplace=True)

        return newmatrix

    def number_galaxies(self):
        galaxies = 1

        for row_id, row in self.matrix.iterrows():
            for col_id, col in row.items():
                if col == GALAXY_STR:
                    newgalaxy = Galaxy(galaxies, row_id, col_id)
                    self.matrix[col_id][row_id] = newgalaxy
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
