#!/usr/bin/env python3


class Set():
    
    def __init__(self, green=0, blue=0, red=0):
        self.green = int(green)
        self.blue = int(blue)
        self.red = int(red)

    def possible(self, reference):
        if self.green > reference.green:
            return False
        if self.blue > reference.blue:
            return False
        if self.red > reference.red:
            return False

        return True

    def power(self):
        return self.green * self.blue * self.red

    @classmethod
    def fromstring(cls, text):
        newset = cls()

        for colorgroup in text.split(','):
            amount = colorgroup.split(' ')[1]
            color = colorgroup.split(' ')[2]
            setattr(newset, color, int(amount))

        return newset

    def __repr__(self):
        return f"green: {self.green}, blue: {self.blue}, red: {self.red}"


class Game():

    def __init__(self, id, sets):
        self.id = int(id)
        self.sets = sets

    def minimalset(self):
        minimalset = Set()

        for set in self.sets:
            if set.green > minimalset.green:
                minimalset.green = set.green
            if set.red > minimalset.red:
                minimalset.red = set.red
            if set.blue > minimalset.blue:
                minimalset.blue = set.blue

        return minimalset

    def possible(self, reference):
        for set in self.sets:
            if not set.possible(reference):
                return False

        return True

    @classmethod
    def fromline(cls, line):
        id = line.split(':')[0].split(' ')[1]
        sets = line.split(':')[1].strip('\n').split(';')

        return cls(int(id), [Set.fromstring(i) for i in sets])

    def __repr__(self):
        return f"{self.id}: " + str(self.sets)


def main():
    games = []
    reference = Set(green=13, blue=14, red=12)
    powers = []

    with open('input', 'r') as f:
        for line in f.readlines():
            games.append(Game.fromline(line))

    for game in games:
        powers.append(game.minimalset().power())

    print(sum(powers))


if __name__ == '__main__':
    main()
