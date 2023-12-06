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
        """In what ways can we win this race?"""

        previous_distance = 0
        for i in range(0, self.time_limit):
            distance = i*(self.time_limit-i)

            if distance < previous_distance and distance < self.record:
                break

            previous_distance = distance

            if distance > self.record:
                self.win_scenarios += 1

    def __repr__(self):
        """Represent a race."""
        return f"time: {self.time_limit}, record: {self.record}"

def main():
    with open('input', 'r') as f:
        text = f.read()

    digits = re.findall(r'[\d]+', text)
    maxtime = int(digits[0])
    record = int(digits[1])

    # This is the flex solution. See the race class for what i used to do. This is 10x as fast tho.
    print(len({i for i in range(0, int(maxtime/2)) if i*(maxtime-i) > record})*2+1)

if __name__ == '__main__':
    main()
