#!/usr/bin/env python3

class Point():
    """Represent a point in the matrix."""

    def __init__(self, char, left=None, up=None, right=None, down=None, is_start=False, is_pipe=False):
        self.char = char
        self.left = left
        self.up = up
        self.right = right
        self.down = down
        self.is_start = is_start
        self.is_pipe = is_pipe
        self.adjacent_pipes = []
        self.row = None
        self.col = None
        self.visited = False

    def is_accessible(self, other):
        """Check if another point is accessible from this point."""
        if self.left:
            if other == self.left:
                if other.char in ['L', '-', 'F']:
                    return True
        if self.right:
            if other == self.right:
                if other.char in ['7', '-', 'J']:
                    return True
        if self.up:
            if other == self.up:
                if other.char in ['|', '7', 'F']:
                    return True
        if self.down:
            if other == self.down:
                if other.char in ['|', 'L', 'J']:
                    return True

        return False

    def update_adjacent_pipes(self):
        """Update what pipes are adjacent."""
        if self.char == '|':
            adjacent_things = [self.up, self.down]
        elif self.char == '-':
            adjacent_things = [self.left, self.right]
        elif self.char == 'L':
            adjacent_things = [self.up, self.right]
        elif self.char == 'J':
            adjacent_things = [self.up, self.left]
        elif self.char == '7':
            adjacent_things = [self.left, self.down]
        elif self.char == 'F':
            adjacent_things = [self.down, self.right]
        else:
            adjacent_things = [self.down, self.right, self.left, self.up]

        adjacent_things = [i for i in adjacent_things if i]
        self.adjacent_pipes = [i for i in adjacent_things if i.is_pipe and self.is_accessible(i)]

    def __eq__(self, other):
        """Compare two instances of this class."""
        return self.row == other.row and self.col == other.col

    def __repr__(self):
        return self.char

class Matrix():
    """Represent our input matrix"""

    def __init__(self):
        self.rows = []
        self.startpoint = None

    def follow(self):
        """Follow pipes from start to start and return the amount of steps."""
        self.startpoint.visited = True
        nextpoint = self.startpoint.adjacent_pipes[0]
        steps = 1

        while True:
            try:
                nextpoint.visited = True
                if nextpoint.adjacent_pipes[0].visited:
                    nextpoint = nextpoint.adjacent_pipes[1]
                else:
                    nextpoint = nextpoint.adjacent_pipes[0]
                steps += 1
                # We're probably done this is ugly but i want to go bouldering
            except IndexError:
                return steps + 1

        return steps

    def create_points(self):
        """Process all rows, creating actual points."""
        for row_id, row in enumerate(self.rows):
            for point_id, c in enumerate(row):
                if c == 'S':
                    is_start = True
                else:
                    is_start = False

                if c in ['|', '-', 'L', 'J', '7', 'F']:
                    is_pipe = True
                else:
                    is_pipe = False

                newpoint = Point(c, is_start=is_start, is_pipe=is_pipe)
                if is_start:
                    self.startpoint = newpoint
                self.rows[row_id][point_id] = newpoint

    def update_points(self):
        """Update all points allocating their neighbours.

        So point.up, point.down, etc. will be references to other points.
        """
        for row_id, row in enumerate(self.rows):
            for point_id, point in enumerate(row):
                point.row = row_id
                point.col = point_id

        for row_id, row in enumerate(self.rows):
            for point_id, point in enumerate(row):
                if point_id > 0:
                    point.left = row[point_id-1]
                if point_id < len(row) - 1:
                    point.right = row[point_id+1]
                if row_id > 0:
                    point.up = self.rows[row_id-1][point_id]
                if row_id < len(self.rows) - 1:
                    point.down = self.rows[row_id+1][point_id]

        for row_id, row in enumerate(self.rows):
            for point in row:
                point.update_adjacent_pipes()

    def __repr__(self):
        return f"{self.rows}"

def main():
    matrix = Matrix()

    with open('input', 'r') as f:
        for line in f.readlines():
            matrix.rows.append([i for i in line.strip()])

    matrix.create_points()
    matrix.update_points()
    steps_roundtrip = matrix.follow()
    print(steps_roundtrip/2)

if __name__ == '__main__':
    main()
