#!/usr/bin/env python3


class Set():
    """Represents a single set in a game."""
    
    def __init__(self, green=0, blue=0, red=0):
        self.green = int(green)
        self.blue = int(blue)
        self.red = int(red)

    def possible(self, reference):
        """Check if a set is possible, against a reference set."""
        if self.green > reference.green:
            return False
        if self.blue > reference.blue:
            return False
        if self.red > reference.red:
            return False

        return True

    @classmethod
    def fromstring(cls, text):
        """Create a set, from a string.
        
        String has to look like: '14 red, 9 green, 5 blue'
        """
        # For jonna: cls() here is the same as using Set() outside of this class.
        # it creates a new instance of a set. Which we later return.
        newset = cls()

        for colorgroup in text.split(','):
            amount = colorgroup.split(' ')[1]
            color = colorgroup.split(' ')[2]
            setattr(newset, color, int(amount))

        return newset

    def __repr__(self):
        return f"green: {self.green}, blue: {self.blue}, red: {self.red}"


class Game():
    """Represents a single game, containing multiple sets."""

    def __init__(self, id, sets):
        self.id = int(id)
        self.sets = sets

    def possible(self, reference):
        """Check if the game is possible.

        Checks a reference set against every set in the game.
        """
        for set in self.sets:
            if not set.possible(reference):
                return False

        return True

    @classmethod
    def fromline(cls, line):
        """Create a game from a complete input line."""
        id = line.split(':')[0].split(' ')[1]
        sets = line.split(':')[1].strip('\n').split(';')

        return cls(int(id), [Set.fromstring(i) for i in sets])

    def __repr__(self):
        return f"{self.id}: " + str(self.sets)


def main():
    games = []
    # We create a reference set that we can check the sets in the game against
    reference = Set(green=13, blue=14, red=12)
    possible_games = []

    # First we just create games from lines
    with open('input', 'r') as f:
        for line in f.readlines():
            games.append(Game.fromline(line))

    # Then we check if a game is possible and add it to the list
    for game in games:
        if game.possible(reference):
            possible_games.append(game.id)

    print(sum(possible_games))


if __name__ == '__main__':
    main()
