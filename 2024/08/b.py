#!/usr/bin/env python
import itertools


class Antenna():

    def __init__(self, frequency, row, pos):
        self.frequency = frequency
        self.row = row
        self.pos = pos

    def __repr__(self):
        return self.frequency


class Map():

    def __init__(self, matrix, antennas, unique_frequencies):
        self.matrix = matrix
        self.antennas = antennas
        self.unique_frequencies = unique_frequencies

    def create_antinode(self, new_row, new_pos):
        if (
            new_row >= 0 and
            new_pos < len(self.matrix[0])
        ):
            return (new_row, new_pos)
        else:
            return False

    def is_inbounds(self, row, pos):
        if row < 0:
            return False
        if row > len(self.matrix)-1:
            return False
        if pos < 0:
            return False
        if pos > len(self.matrix[0])-1:
            return False
        return True

    def trace_line(self, origin_antenna, dest_antenna):
        new_antinodes = [
            (origin_antenna.row, origin_antenna.pos),
            (dest_antenna.row, dest_antenna.pos)
        ]

        if origin_antenna.row == dest_antenna.row:
            row_diff = 0
        elif abs(origin_antenna.row - dest_antenna.row) == 1:
            row_diff = 1
        else:
            row_diff = abs(origin_antenna.row - dest_antenna.row)

        if origin_antenna.pos == dest_antenna.pos:
            pos_diff = 0
        elif abs(origin_antenna.pos - dest_antenna.pos) == 1:
            pos_diff = 1
        else:
            pos_diff = abs(origin_antenna.pos - dest_antenna.pos)

        if origin_antenna.row > dest_antenna.row:
            row_diff = -row_diff
        if origin_antenna.pos > dest_antenna.pos:
            pos_diff = -pos_diff

        next_row = dest_antenna.row + row_diff
        next_pos = dest_antenna.pos + pos_diff
        inbounds = self.is_inbounds(next_row, next_pos)

        while inbounds:
            newnode = (next_row, next_pos)
            new_antinodes.append(newnode)
            next_row = next_row + row_diff
            next_pos = next_pos + pos_diff
            inbounds = self.is_inbounds(next_row, next_pos)

        return new_antinodes

    def find_antinodes(self):
        antinodes = []

        for freq in self.unique_frequencies:
            antennae_infreq = [i for i in self.antennas if i.frequency == freq]
            combinations = [i for i in list(
                itertools.permutations(antennae_infreq, 2)
            )]

            for antenna1, antenna2 in combinations:
                antinodes = antinodes + self.trace_line(antenna1, antenna2)

        for row, pos in antinodes:
            self.matrix[row][pos] = '#'

        return antinodes

    @classmethod
    def from_file(cls):
        antennas = []
        matrix = []
        unique_frequencies = []

        with open('input', 'r') as f:
            for row, line in enumerate(f.readlines()):
                newline = []
                for pos, char in enumerate(line.strip()):
                    if char == '.':
                        newline.append('.')
                    else:
                        newantenna = Antenna(char, row, pos)
                        antennas.append(newantenna)
                        newline.append(newantenna)
                        if char not in unique_frequencies:
                            unique_frequencies.append(char)

                matrix.append(newline)

        return cls(
            matrix,
            antennas,
            unique_frequencies,
        )

    def __repr__(self):
        out = ""
        for row in self.matrix:
            for char in row:
                out = out + str(char)
            out = out + "\n"
        return out


def main():
    map = Map.from_file()
    print(len(set(map.find_antinodes())))
    print(map)


if __name__ == '__main__':
    main()
