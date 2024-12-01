#!/usr/bin/env python3
import re

numbermap = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def replace_numberwords(line_in):
    inserts = {}
    inserts_done = 0
    for word in numbermap:
        inserts[word] = [m.start() for m in re.finditer(word, line_in)]

    for word in inserts:
        for place in inserts[word]:
            line_in = line_in[:place+inserts_done] + str(numbermap[word]) + line_in[place+inserts_done:]
            inserts_done += 1

    return line_in

def extract_numbers(line_in):
    numbers = []

    for c in line_in:
        try:
            numbers.append(int(c))
        except ValueError:
            pass

    return numbers

def make_set(numberlist):
    firstlast = [str(numberlist[0]), str(numberlist[-1])]
    return ''.join(firstlast)

def main():
    number_lists = []
    total = 0

    with open('input', 'r') as f:
        for line in f.readlines():
            number_lists.append(extract_numbers(replace_numberwords(line)))

    for list in number_lists:
        total += int(make_set(list))

    print(total)

if __name__ == '__main__':
    main()
