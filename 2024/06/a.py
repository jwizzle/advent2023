#!/usr/bin/env python
from enum import Enum


class GuardDirection(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'


class EmptyOccupant():

    def __init__(self):
        self.notation = '.'

    def __repr__(self):
        return self.notation


class Obstruction(EmptyOccupant):

    def __init__(self):
        self.notation = '#'


class Guard(EmptyOccupant):

    def __init__(self, direction):
        self.direction = direction
        self.notation = self.get_notation()

    def get_notation(self):
        if self.direction == GuardDirection.NORTH:
            return '^'
        elif self.direction == GuardDirection.SOUTH:
            return 'v'
        elif self.direction == GuardDirection.EAST:
            return '>'
        else:
            return '<'

    def destination_from_direction(self, cur_x, cur_y, direction):
        if direction == GuardDirection.NORTH:
            return (cur_x-1, cur_y)
        elif direction == GuardDirection.SOUTH:
            return (cur_x+1, cur_y)
        elif direction == GuardDirection.EAST:
            return (cur_x, cur_y+1)
        else:
            return (cur_x, cur_y-1)

    def find_valid_direction(self, mapsquares, cur_x, cur_y, cur_dir):
        if cur_dir == GuardDirection.NORTH:
            if isinstance(mapsquares[cur_x-1][cur_y].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.EAST
                )
            else:
                return cur_dir
        elif cur_dir == GuardDirection.SOUTH:
            if isinstance(mapsquares[cur_x+1][cur_y].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.WEST
                )
            else:
                return cur_dir
        elif cur_dir == GuardDirection.EAST:
            if isinstance(mapsquares[cur_x][cur_y+1].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.SOUTH
                )
            else:
                return cur_dir
        else:
            if isinstance(mapsquares[cur_x][cur_y-1].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.NORTH
                )
            else:
                return cur_dir


class MapSquare():

    def __init__(self, x, y, occupant, visited=False):
        self.x = x
        self.y = y
        self.occupant = occupant
        self.visited = visited

    def __repr__(self):
        return str(self.occupant)


class Map():

    def __init__(self, squares, matrix):
        self.squares = squares
        self.matrix = matrix

    def patrol_guard(self):
        guardsquare = [
            sq for sq in self.squares if isinstance(
                sq.occupant, Guard)
        ][0]
        guard = guardsquare.occupant
        newdirection = guard.find_valid_direction(
            self.matrix, guardsquare.x, guardsquare.y, guard.direction
        )
        guard.direction = newdirection
        self.move_object(
            guard,
            (guardsquare.x, guardsquare.y),
            guard.destination_from_direction(
                guardsquare.x,
                guardsquare.y,
                newdirection
            )
        )

    def move_object(self, movable, origin, destination):
        old_x, old_y = origin
        new_x, new_y = destination

        self.matrix[old_x][old_y].visited = True
        self.matrix[old_x][old_y].occupant = EmptyOccupant()
        self.matrix[new_x][new_y].occupant = movable

    @classmethod
    def from_file(cls, file):
        mapsquares = []
        matrix = []

        for x, line in enumerate(file.readlines()):
            newline = []

            for y, char in enumerate(line):
                if char == '#':
                    newoccupant = Obstruction()
                elif char == '^':
                    newoccupant = Guard(GuardDirection.NORTH)
                else:
                    newoccupant = EmptyOccupant()

                newsquare = MapSquare(x, y, newoccupant)
                newline.append(newsquare)
                mapsquares.append(newsquare)

            matrix.append(newline)

        return cls(
            mapsquares,
            matrix,
        )

    def __repr__(self):
        out = ''
        for line in self.matrix:
            for square in line:
                out = out + str(square)
            out = out + '\n'

        return out


def main():
    with open('input', 'r') as f:
        map = Map.from_file(f)

    while True:
        try:
            map.patrol_guard()
        except IndexError:
            print(len([i for i in map.squares if i.visited]) + 1)
            exit()


if __name__ == '__main__':
    main()
