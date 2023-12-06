#!/usr/bin/env python3
import re

class Race():
    """Represent a single race."""

    def __init__(self, time_limit, record):
        """Construct the race."""
        self.time_limit = int(time_limit)
        self.record = int(record)
        self.win_scenarios = 0

    def check_win_scenarios(self):
        """In what ways can we win this race?

        The commented out lines are my initial solution. For reference.
        The current code being the fastest i've come up with. For the flex.
        There's probably some math-wizard solution i'm still missing as well.
        """
        self.win_scenarios = len({i for i in range(0, int(self.time_limit/2)) if i*(self.time_limit-i) > self.record})*2+1

#        previous_distance = 0
#        for i in range(0, self.time_limit):
#            distance = i*(self.time_limit-i)
#
#            if distance < previous_distance and distance < self.record:
#                break
#
#            previous_distance = distance
#
#            if distance > self.record:
#                self.win_scenarios += 1

    def __repr__(self):
        """Represent a race."""
        return f"time: {self.time_limit}, record: {self.record}"

def main():
    with open('input', 'r') as f:
        text = f.read()

    digits = re.findall(r'[\d]+', text)
    maxtimes = digits[0:int(len(digits)/2)]
    records = digits[int(len(digits)/2):len(digits)]
    races = [Race(time_limit, record) for time_limit, record in zip(maxtimes, records)]

    for race in races:
        race.check_win_scenarios()

    out = 1
    for race in races:
        out = out * race.win_scenarios

    print(out)

if __name__ == '__main__':
    main()
