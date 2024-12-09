#!/usr/bin/env python
import itertools
import operator
from multiprocessing import Pool


def isoperator(char):
    try:
        int(char)
        return False
    except ValueError:
        return True


def concatenate(string1, string2):
    return int("{}{}".format(string1, string2))


class Equation():

    def __init__(self, test_value, spots):
        self.test_value = int(test_value)
        self.spots = spots
        self.possible_ops = '+*|'

    def calculate(self):
        out = 0
        op = operator.add

        for i in self.spots:
            if i == '+':
                op = operator.add
            elif i == '*':
                op = operator.mul
            elif i == '|':
                op = concatenate
            else:
                out = op(out, int(i))

        return out

    def is_valid(self):
        return self.calculate() == self.test_value

    def solve(self):
        operators = [
            i for i in self.spots if isoperator(i)
        ]
        combinations = [''.join(i) for i in list(
            itertools.product(self.possible_ops, repeat=len(operators))
        )]

        for combination in combinations:
            comblist = [i for i in combination]
            new_spots = [i for i in self.spots]
            for id, spot in enumerate(new_spots):
                if isoperator(spot):
                    new_spots[id] = comblist.pop(0)

            new_equation = Equation(
                self.test_value,
                new_spots
            )

            if new_equation.is_valid():
                return new_equation.test_value

    @classmethod
    def from_line(cls, linetext):
        testvalue = linetext.split(': ')[0]
        input_spots = []
        for i in linetext.split(': ')[1].split(' '):
            input_spots.append(i)
            input_spots.append('+')

        del input_spots[-1]

        return cls(testvalue, input_spots)

    def __repr__(self):
        out = ""
        for spot in self.spots:
            out = out + str(spot)
        return out


def loop_equations(equation):
    return equation.solve()


def main():
    equations = []
    with open('input', 'r') as f:
        for line in f.readlines():
            equations.append(Equation.from_line(line.strip()))

    with Pool(12) as p:
        outlist = p.map(loop_equations, equations)

    print(sum([int(i) for i in outlist if i]))


if __name__ == '__main__':
    main()
