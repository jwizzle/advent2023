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

    def find_antinodes(self):
        antinodes = []

        for freq in self.unique_frequencies:
            antennae_infreq = [i for i in self.antennas if i.frequency == freq]
            combinations = [i for i in list(
                itertools.combinations(antennae_infreq, 2)
            )]
            for antenna1, antenna2 in combinations:
                # Antinode 1 is always a line from 1 to behind antenna 2
                # Antinode 2 is always a line from 2 to behind antenna 1
                #
                if antenna1.row < antenna2.row:
                    # Antenna 2 is south
                    anti1_row = antenna2.row + len(list(range(
                        antenna1.row, antenna2.row)))
                    anti2_row = antenna1.row - len(list(range(
                        antenna1.row, antenna2.row)))
                elif antenna1.row > antenna2.row:
                    # Antenna 2 is north
                    anti1_row = antenna1.row - len(list(range(
                        antenna1.row1, antenna2.row)))
                    anti2_row = antenna2.row + antenna1.row
                else:
                    anti1_row = antenna2.row
                    anti2_row = antenna2.row

                if antenna1.pos < antenna2.pos:
                    # Antenna 2 east
                    anti1_pos = antenna2.pos + antenna2.pos - antenna1.pos
                    anti2_pos = antenna1.pos - (antenna2.pos - antenna1.pos)
                elif antenna1.pos > antenna2.pos:
                    # Antenna 2 west
                    anti1_pos = antenna2.pos + antenna2.pos - antenna1.pos
                    anti2_pos = (antenna1.pos - antenna2.pos) + antenna1.pos
                else:
                    anti1_pos = antenna2.pos
                    anti2_pos = antenna2.pos

                if (
                    anti1_row >= 0 and
                    anti1_row < len(self.matrix) and
                    anti1_pos >= 0 and
                    anti1_pos < len(self.matrix[0])
                ):
                    antinodes.append((anti1_row, anti1_pos))

                if (
                    anti2_row >= 0 and
                    anti2_row < len(self.matrix) and
                    anti2_pos >= 0 and
                    anti2_pos < len(self.matrix[0])
                ):
                    antinodes.append((anti2_row, anti2_pos))

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
        return out


def main():
    map = Map.from_file()
    print(map.find_antinodes())
    print(len(set(map.find_antinodes())))


if __name__ == '__main__':
    main()
