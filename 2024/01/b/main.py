#!/usr/env python

def main():
    leftlist = []
    rightlist = []

    with open('input', 'r') as f:
        for line in f.readlines():
            splitline = line.split(' ')
            leftlist.append(int(splitline[0]))
            rightlist.append(int(splitline[1]))

    resultlist = [
        rightlist.count(i)*i for i in leftlist
    ]

    print(sum(resultlist))


if __name__ == '__main__':
    main()
