#!/usr/bin/env python3
import re

class Boat():
    """Represent a raceboat."""

    def __init__(self, time_held):
        """Construct the boat."""
        self.startspeed = 0
        self.increase_per_ms = 1
        self.time_held = time_held
        self.speed = time_held*self.increase_per_ms

    def distance(self, time):
        """Get the distance traveled in given time."""
        return time*self.speed

class Race():
    """Represent a single race."""

    def __init__(self, time_limit, record):
        """Construct the race."""
        self.time_limit = int(time_limit)
        self.record = int(record)
        self.win_scenarios = 0

    def check_win_scenarios(self):
        """In what ways can we win this race?"""
        possibilities = [False]*self.time_limit

        for id, possibility in enumerate(possibilities):
            boat = Boat(id)
            traveldistance = boat.distance(self.time_limit - id)
            if traveldistance > self.record: possibilities[id] = True

        self.win_scenarios = len([i for i in possibilities if i])

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
