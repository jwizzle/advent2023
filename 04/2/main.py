#!/usr/bin/env python3
import re

class Card():
    """Represents one single scratch card."""

    def __init__(self, id, numbers, w_numbers):
        """Construct the card."""
        self.id = id
        self.numbers = numbers
        self.w_numbers = w_numbers
        self.points = self.__points()

    def __points(self):
        """Check the amount of points for this card."""
        points = 0

        for n in self.numbers:
            if n in self.w_numbers:
                points += 1

        return points

    def process(self, cards):
        """Process the card, tallying amounts of new cards.

        We do this once per type of card, so we use the amount of cards
        there are of this type to multiply everything we do.
        """
        # We exit early if there's no points
        if self.points == 0: return False

        # The type of card we are now processing has an amount already.
        # Instead of processing every card, we just add the amount of cards
        # we already have to the underlying cards. This saves a shitton of CPU/processing.
        #
        # Cards is passed by reference making the tallying itself possible.
        # ask me to explain reference if you don't know wtf that means.
        for i in range(1, self.points+1):
            newid = self.id + i
            to_add = cards[self.id]['amount']
            try:
                cards[newid]['amount'] += to_add
            # If we get a key error then we are out of range, and probably done
            except KeyError:
                return True

        return True

    @classmethod
    def from_line(cls, line):
        """Create a card from a given line of text."""
        id = int(re.findall(r'[\d]+', line.split(':')[0])[0])
        numbers = [int(i) for i in line.split(':')[1].split('|')[1].split(' ') if i]
        w_numbers = [int(i) for i in line.split(':')[1].split('|')[0].split(' ') if i]

        return cls(id, numbers, w_numbers)

    def __repr__(self):
        return f"Card {self.id}"


def main():
    cards = {}

    # This time we make a dictionary of cards and how many there are
    # Since keeping lists of growing cards eats memory.
    # At the start this is only 1 card
    with open('input', 'r') as f:
        for line in f.readlines():
            newcard = Card.from_line(line.strip())
            cards[newcard.id] = {'reference': newcard, 'amount': 1}

    # We just process every card once and give our current collection
    # of cards so we can tally in the .process() function.
    for id in cards:
        cards[id]['reference'].process(cards)

    print(sum([cards[i]['amount'] for i in cards]))

if __name__ == '__main__':
    main()
