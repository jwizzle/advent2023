#!/usr/env python

def main():
    leftlist = []
    rightlist = []

    with open('input', 'r') as f:
        for line in f.readlines():
            splitline = line.split(' ')
            leftlist.append(int(splitline[0]))
            rightlist.append(int(splitline[1]))

    leftlist.sort()
    rightlist.sort()
    resultlist = [
        abs(i - rightlist[id]) for id, i in enumerate(leftlist)
    ]

    print(sum(resultlist))


if __name__ == '__main__':
    main()
