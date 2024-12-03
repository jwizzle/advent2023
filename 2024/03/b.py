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
    insruction_regex = r"(do|don't|mul)\((\d{1,3},\d{1,3})?\)"
    processing = True

    with open('input', 'r') as f:
        for line in f.readlines():
            for instruction, content in re.findall(insruction_regex, line):
                if instruction == 'mul':
                    if processing:
                        instructions.append(MulInstruction(content))
                elif instruction == "don't":
                    processing = False
                elif instruction == "do":
                    processing = True

    print(sum([i.result() for i in instructions]))


if __name__ == '__main__':
    main()
