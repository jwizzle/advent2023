#!/usr/bin/env python


def split_even(number):
    numberstring = str(number)
    stringlength = len(str(number))
    leftstone = int(numberstring[:stringlength//2])
    rightstone = int(numberstring[stringlength//2:])
    return leftstone, rightstone


def process_stones(stones):
    newstones = {}

    # Process zeroes
    if 0 in stones:
        zeroes = stones[0]
        if 1 not in newstones:
            newstones[1] = 0
        newstones[1] += zeroes

    # Process evens
    evens = {
        k: stones[k] for k in stones if len(str(k)) % 2 == 0
    }
    for even in evens:
        stone1, stone2 = split_even(even)

        if stone1 not in newstones:
            newstones[stone1] = 0
        if stone2 not in newstones:
            newstones[stone2] = 0

        newstones[stone1] += evens[even]
        newstones[stone2] += evens[even]

    # Process the rest
    unique_numbers = {
        k*2024: stones[k] for k in stones if k != 0 and len(str(k)) % 2 != 0
    }
    for number in unique_numbers:
        if number not in newstones:
            newstones[number] = 0
        newstones[number] += unique_numbers[number]

    return newstones


def main():
    stones = {}

    with open('input', 'r') as f:
        for line in f.readlines():
            for stone in line.strip().split(' '):
                stones[(int(stone))] = 1

    for i in range(1, 76):
        stones = process_stones(stones)

    print(sum([stones[stone] for stone in stones if stones[stone] > 0]))


if __name__ == '__main__':
    main()
