#!/usr/bin/env python
import re


class MulInstruction():
    def __init__(self, text):
        integers = re.findall(r"\d+", text)
        self.int_a = int(integers[0])
        self.int_b = int(integers[1])

    def result(self):
        return self.int_a * self.int_b


def main():
    instructions = []

    with open('input', 'r') as f:
        for line in f.readlines():
            for mul in re.findall(r"mul\(\d{1,3},\d{1,3}\)", line):
                instructions.append(MulInstruction(mul))

    print(sum([i.result() for i in instructions]))


if __name__ == '__main__':
    main()
