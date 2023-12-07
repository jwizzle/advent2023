#!/usr/bin/env python3

card_valuemap = { 'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1 }
hand_valuemap = {
    'fivekind': 7,
    'fourkind': 6,
    'fullhouse': 5,
    'threekind': 4,
    'twopair': 3,
    'onepair': 2,
    'highcard': 1,
}

class Card():
    """Represent a card."""

    def __init__(self, symbol):
        self.symbol = symbol
        self.reference_value = card_valuemap[symbol]

    def __repr__(self):
        return f"{self.symbol}"


class Hand():
    """Represent a hand."""

    def __init__(self, bid):
        self.handtype = False
        self.cards = []
        self.bid = int(bid)

    def get_type(self):
        """Get the type of this hand. Five of a kind, four of, etc."""
        cardlist = [i.symbol for i in self.cards]

        if len(set(cardlist)) == 1:
            return 'fivekind'

        duplicates = list(set([sym for sym in cardlist if cardlist.count(sym) > 1]))

        if not duplicates:
            return 'highcard'
        elif len(duplicates) == 2:
            dupeone_count = cardlist.count(duplicates[0])
            dupetwo_count = cardlist.count(duplicates[1])

            if dupeone_count == 2 and dupetwo_count == 3:
                return 'fullhouse'
            if dupetwo_count == 2 and dupeone_count == 3:
                return 'fullhouse'
            if dupeone_count == 2 and dupetwo_count == 2:
                return 'twopair'
        else:
            dupecount = cardlist.count(duplicates[0])
            if dupecount == 2:
                return 'onepair'
            if dupecount == 3:
                return 'threekind'
            if dupecount == 4:
                return 'fourkind'

    @classmethod
    def fromline(cls, line):
        """Create a hand from a line of input text."""
        cardtext = line.split(' ')[0]
        bid = line.split(' ')[1]

        newhand = cls(bid)
        newhand.cards = [Card(c) for c in cardtext]
        newhand.handtype = newhand.get_type()

        return newhand

    def __lt__(self, other):
        """Less than '<' comparison."""
        if hand_valuemap[self.handtype] == hand_valuemap[other.handtype]:
            for id, card in enumerate(self.cards):
                if card.reference_value != other.cards[id].reference_value:
                    return card.reference_value < other.cards[id].reference_value

        return hand_valuemap[self.handtype] < hand_valuemap[other.handtype]

    def __repr__(self):
        return f"{self.cards}"


def main():
    hands = []

    with open('input', 'r') as f:
        for line in f.readlines():
            hands.append(Hand.fromline(line))

    hands.sort()

    total = 0
    for id, hand in enumerate(hands):
        rank = id+1
        total += hand.bid * rank

    print(total)

if __name__ == '__main__':
    main()
