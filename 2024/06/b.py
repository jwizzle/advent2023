#!/usr/bin/env python
from enum import Enum
import copy
from multiprocessing import Pool
import itertools
from functools import partial


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

    def __init__(self, notation='#'):
        self.notation = notation


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
            if cur_x - 1 < 0:
                return cur_dir
            if isinstance(mapsquares[cur_x-1][cur_y].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.EAST
                )
            else:
                return cur_dir
        elif cur_dir == GuardDirection.SOUTH:
            if cur_x + 1 > len(mapsquares) - 1:
                return cur_dir
            if isinstance(mapsquares[cur_x+1][cur_y].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.WEST
                )
            else:
                return cur_dir
        elif cur_dir == GuardDirection.EAST:
            if cur_y + 1 > len(mapsquares[0]) - 1:
                return cur_dir
            if isinstance(mapsquares[cur_x][cur_y+1].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.SOUTH
                )
            else:
                return cur_dir
        else:
            if cur_y - 1 < 0:
                return cur_dir
            if isinstance(mapsquares[cur_x][cur_y-1].occupant, Obstruction):
                return self.find_valid_direction(
                    mapsquares, cur_x, cur_y, GuardDirection.NORTH
                )
            else:
                return cur_dir


class MapSquare():

    def __init__(self, x, y, occupant, visited=0):
        self.x = x
        self.y = y
        self.occupant = occupant
        self.visited = visited

    def __repr__(self):
        if self.visited:
            return 'X'
        else:
            return str(self.occupant)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Map():

    def __init__(self, squares, matrix):
        self.squares = squares
        self.matrix = matrix
        self.guardsquare = self.get_guardsquare()

    def get_guardsquare(self):
        return [
            sq for sq in self.squares if isinstance(
                sq.occupant, Guard)
        ][0]

    def patrol_guard(self):
        guardsquare = self.guardsquare
        guard = guardsquare.occupant
        newdirection = guard.find_valid_direction(
            self.matrix, guardsquare.x, guardsquare.y, guard.direction
        )

        guard.direction = newdirection
        if not self.move_object(
            guard,
            (guardsquare.x, guardsquare.y),
            guard.destination_from_direction(
                guardsquare.x,
                guardsquare.y,
                newdirection
            )
        ):
            return False
        else:
            return max([sq.visited for sq in self.squares])

    def move_object(self, movable, origin, destination):
        old_x, old_y = origin
        new_x, new_y = destination

        if (
            new_x < 0 or
            new_y < 0 or
            new_x > len(self.matrix) - 1 or
            new_y > len(self.matrix[0]) - 1
        ):
            return False

        self.matrix[old_x][old_y].occupant = EmptyOccupant()
        self.matrix[new_x][new_y].occupant = movable
        self.matrix[new_x][new_y].visited += 1
        self.guardsquare = self.matrix[new_x][new_y]

        return True

    @classmethod
    def from_file(cls, file):
        mapsquares = []
        matrix = []

        for x, line in enumerate(file.readlines()):
            newline = []

            for y, char in enumerate(line.strip()):
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


def find_loopingmaps(sq, original_map):
    fakemap = copy.deepcopy(original_map)
    fakemap.matrix[sq.x][sq.y].occupant = Obstruction(notation='O')
    while True:
        patrolresult = fakemap.patrol_guard()
        if not patrolresult:
            return False
        elif patrolresult > 3:
            return fakemap


def main():
    with open('input', 'r') as f:
        map = Map.from_file(f)

    original_map = copy.deepcopy(map)

    while map.patrol_guard():
        pass

    visited_squares = [
        sq for sq in map.squares if (
            sq.visited and sq != original_map.guardsquare
        )
    ]

    partial_function = partial(find_loopingmaps, original_map=original_map)
    with Pool(12) as p:
        looping_maps = p.map(
            partial_function, visited_squares
        )

    print(len([map for map in looping_maps if map]))


if __name__ == '__main__':
    main()
