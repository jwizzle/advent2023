#!/usr/bin/env python3

class MapEntry():
    """Represent a single entry in a map."""

    def __init__(self, dst_start, src_start, length):
        """Construct the entry."""
        self.dst_start = int(dst_start)
        self.src_start = int(src_start)
        self.length = int(length)

    @classmethod
    def from_line(cls, line):
        """Create a map entry from a line of text."""
        elements = line.split(' ')
        return cls(elements[0], elements[1], elements[2])

    def __repr__(self):
        return f"{self.dst_start, self.src_start, self.length}"


class Map():
    """Represent a map of different categories."""

    def __init__(self, source, destination):
        """Construct the map."""
        self.entries = []
        self.source = source
        self.destination = destination

    def get_destination(self, input):
        """Get the destination of input. Can be seed, soil, etc.

        Basically we just check if a number falls between the start and end.
        If it does we use the difference between the source and input, and
        use that to determine the destination.
        """
        for entry in self.entries:
            last_num = entry.src_start + entry.length - 1

            if input <= last_num and input >= entry.src_start:
                diff = input - entry.src_start
                return entry.dst_start + diff

        # If we reach this the input is not mapped
        return input

    def __repr__(self):
        return f"{self.source}-to-{self.destination}: {self.entries}"


class Almanac():
    """Represent a complete almanac with data."""

    def __init__(self):
        """Construct the almanac."""
        self.seeds = []
        self.maps = []

    def resolve_location(self, seed):
        """Resolve the location of a seed."""
        map_in = seed

        for map in self.maps:
            map_in = map.get_destination(map_in)

        return map_in

    @classmethod
    def from_text(cls, text):
        """Generate a complete almanac from our input."""
        new_almanac = cls()
        seedline = text.split('\n')[0]

        # parse seeds
        for seed in seedline.split(':')[1].split(' ')[1:]:
            new_almanac.seeds.append(int(seed))

        # Parse our maps, ignoring the seed line and blank line
        for line in text.split('\n')[2:]:
            # We reached the end of a map, add it and skip this iteration
            if not line:
                new_almanac.maps.append(newmap)
                continue

            # We start processing a new map if it doesn't start with a digit
            if not line[0].isdigit():
                src_dst = line.split(' ')[0].split('-to-')
                newmap = Map(src_dst[0], src_dst[1])
            # We add an entry to the map we're processing if it does
            else:
                newmap.entries.append(MapEntry.from_line(line))
                    
        return new_almanac

    def __repr__(self):
        return f"{self.maps}"


def main():
    with open('input', 'r') as f:
        almanac = Almanac.from_text(f.read())

    locations = []
    for seed in almanac.seeds:
        locations.append(almanac.resolve_location(seed))

    locations.sort()

    print(locations[0])

if __name__ == '__main__':
    main()
