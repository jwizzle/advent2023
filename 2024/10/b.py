#!/usr/bin/env python


class Position():

    def __init__(self, row, pos, height):
        self.row = row
        self.pos = pos
        self.height = height

    def find_neighbours(self, matrix):
        neighbours = []
        south_isvalid = self.row + 1 < len(matrix)
        north_isvalid = self.row - 1 >= 0
        east_isvalid = self.pos + 1 < len(matrix[0])
        west_isvalid = self.pos - 1 >= 0

        if south_isvalid:
            neighbours.append(matrix[self.row+1][self.pos])
        if north_isvalid:
            neighbours.append(matrix[self.row-1][self.pos])
        if east_isvalid:
            neighbours.append(matrix[self.row][self.pos+1])
        if west_isvalid:
            neighbours.append(matrix[self.row][self.pos-1])

        return neighbours

    def find_next_positions(self, matrix):
        possible_positions = []

        for neighbour in self.find_neighbours(matrix):
            if neighbour.height == self.height + 1:
                possible_positions.append(neighbour)

        return possible_positions

    def walk(self, matrix):
        possible_positions = self.find_next_positions(matrix)

        if self.height == 9:
            yield self
        elif possible_positions:
            for position in possible_positions:
                yield from position.walk(matrix)
        else:
            yield None

    def __repr__(self):
        return str(self.height)


class TrailHead(Position):

    def __init__(self, row, pos, height):
        super().__init__(row, pos, height)
        self.trails = []

    def find_valid_trails(self, matrix):
        return [
            trail for trail in self.walk(matrix) if trail
        ]

    def get_score(self):
        return len(self.trails)


class Map():

    def __init__(self, matrix):
        self.matrix = matrix
        self.trailheads = [
            i for row in matrix for i in row if isinstance(i, TrailHead)
        ]

    def find_trails(self):
        for trailhead in self.trailheads:
            trailhead.trails = trailhead.find_valid_trails(self.matrix)

    @classmethod
    def from_file(cls):
        matrix = []

        with open('input', 'r') as f:
            for row, line in enumerate(f.readlines()):
                newline = []
                for pos, char in enumerate(line.strip()):
                    height = int(char)
                    if height == 0:
                        newpos = TrailHead(row, pos, height)
                    else:
                        newpos = Position(row, pos, height)

                    newline.append(newpos)

                matrix.append(newline)

        return cls(
            matrix
        )

    def __repr__(self):
        out = ""
        for row in self.matrix:
            for pos in row:
                out += str(pos)
            out += "\n"

        return out


def main():
    map = Map.from_file()
    map.find_trails()
    print(sum([i.get_score() for i in map.trailheads]))


if __name__ == '__main__':
    main()
