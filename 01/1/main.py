#!/usr/bin/env python3

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
            number_lists.append(extract_numbers(line))

    for list in number_lists:
        total += int(make_set(list))

    print(total)

if __name__ == '__main__':
    main()
