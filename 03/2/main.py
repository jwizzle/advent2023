#!/usr/bin/env python3

class Gear():

    def __init__(self, row, pos, numbers):
        self.row = row
        self.pos = pos
        self.numbers = numbers
        self.value = 0

    def update_value(self):
        self.value = self.numbers[0].value * self.numbers[1].value

    def __eq__(self, other):
        if self.row == other.row and self.pos == other.pos:
            return True
        else:
            return False

    def __repr__(self):
        return f"row: {self.row}, pos: {self.row}, num: {self.numbers}"

class Number():

    def __init__(self, value, row, start_pos, end_pos):
        self.value = value
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.row = row
        self.adjacent_gears = []
        self.part = False

    def update_part_status(self, matrix):
        adjacent = []
        rows = []
        if self.row > 0: rows.append(self.row-1)
        if self.row < len(matrix)-1: rows.append(self.row+1)

        for row in rows:
            for c in range(self.start_pos-1, self.end_pos+2):
                try:
                    if c != -1: adjacent.append(matrix[row][c])
                except IndexError:
                    pass

        if self.start_pos > 0: adjacent.append(matrix[self.row][self.start_pos-1])
        if self.end_pos != len(matrix[self.row])-1: adjacent.append(matrix[self.row][self.end_pos+1])

        for c in adjacent:
            if c != '.' and not is_number(c):
                self.part = True
                return True

    def update_gears(self, matrix):
        adjacent = []
        rows = []
        if self.row > 0: rows.append(self.row-1)
        if self.row < len(matrix)-1: rows.append(self.row+1)

        for row in rows:
            for c in range(self.start_pos-1, self.end_pos+2):
                try:
                    if c != -1: adjacent.append({matrix[row][c]: {'row': row, 'pos': c}})
                except IndexError:
                    pass

        if self.start_pos > 0: adjacent.append(
            {matrix[self.row][self.start_pos-1]: {'row': self.row, 'pos': self.start_pos-1}})
        if self.end_pos != len(matrix[self.row])-1: adjacent.append(
            {matrix[self.row][self.end_pos+1]: {'row': self.row, 'pos': self.end_pos+1}})

        for c in adjacent:
            if '*' in c.keys():
                self.adjacent_gears.append(Gear(c['*']['row'], c['*']['pos'], [self]))

    def __repr__(self):
        return f"{self.value}"


class Schematic():

    def __init__(self):
        self.numbers = []
        self.rows = []
        self.gears = []
        self.parts = []

    def find_parts(self):
        for n in self.numbers:
            n.update_part_status(self.rows)

        self.parts = [x for x in self.numbers if x.part]

    def find_gears(self):
        gears = []

        for n in self.parts:
            n.update_gears(self.rows)

            for gear in n.adjacent_gears:
                if gear not in gears:
                    gears.append(gear)
                else:
                    for existinggear in gears:
                        if gear == existinggear:
                            existinggear.numbers.append(n)

        self.gears = [i for i in gears if len(i.numbers) == 2]

    def add_row(self, row):
        self.rows.append(row)
        number = ''
        start_pos = 0
        creating_number = False

        for index, c in enumerate(row):
            if not creating_number:
                if is_number(c):
                    number += c
                    start_pos = index
                    creating_number = True
            else:
                if is_number(c):
                    number += c
                else:
                    self.numbers.append(Number(int(number), len(self.rows)-1, start_pos, index-1))
                    number = ''
                    creating_number = False

        if creating_number:
            self.numbers.append(Number(int(number), len(self.rows)-1, start_pos, len(row)-1))


    def __repr__(self):
        return str(self.rows)


def is_number(character):
    if character == '0':
        return True
    try:
        return int(character)
    except ValueError:
        return False

def main():
    scheme = Schematic()

    with open('input', 'r') as f:
        for line in f.readlines():
            scheme.add_row(line.strip())

    scheme.find_parts()
    scheme.find_gears()
    for gear in scheme.gears:
        gear.update_value()

    print(sum(i.value for i in scheme.gears))

if __name__ == '__main__':
    main()
