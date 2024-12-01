#!/usr/bin/env python3

class Card():
    """Represents one single scratch card."""

    def __init__(self, id, numbers, w_numbers):
        """Construct the card."""
        self.id = id
        self.numbers = numbers
        self.w_numbers = w_numbers
        self.points = 0

    def process(self):
        """Process the card, checking winning numbers and calculating points."""
        for n in self.numbers:
            if n in self.w_numbers:
                if self.points == 0:
                    self.points += 1
                else:
                    self.points = self.points * 2

    @classmethod
    def from_line(cls, line):
        """Create a card from a given line of text."""
        id = line.split(':')[0].split(' ')[1]
        numbers = [int(i) for i in line.split(':')[1].split('|')[1].split(' ') if i]
        w_numbers = [int(i) for i in line.split(':')[1].split('|')[0].split(' ') if i]

        return cls(id, numbers, w_numbers)

    def __repr__(self):
        return f"Card {self.id}: {self.w_numbers} | {self.numbers}"


def main():
    cards = []

    with open('input', 'r') as f:
        for line in f.readlines():
            cards.append(Card.from_line(line.strip()))

    for card in cards:
        card.process()

    print(sum([i.points for i in cards]))

if __name__ == '__main__':
    main()
