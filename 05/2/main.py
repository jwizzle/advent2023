#!/usr/bin/env python3

class MapEntry():
    """Represent a single entry in a map."""

    def __init__(self, dst_start, src_start, length):
        """Construct the entry."""
        self.dst_start = int(dst_start)
        self.src_start = int(src_start)
        self.length = int(length)

    def src_from_dst(self, dst):
        """Get a matching src for a dst in this range. Or false."""
        last_num = self.dst_start + self.length - 1

        if dst <= last_num and dst >= self.dst_start:
            diff = dst - self.dst_start
            return self.src_start + diff
        else:
            return False

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

    def shortest_path_to(self, destinationlist):
        """Find the shortest paths to entries in a given list."""
        if destinationlist:
            optimal_src_range = []
            for destination in enumerate(destinationlist):
                needed_input = destination

                for entry in self.entries:
                    if entry.src_from_dst(destination):
                        needed_input = entry.src_from_dst(destination)
                        break

                optimal_src_range.append(needed_input)
        #This is probably the location map
        else:
            optimal_entries = [i.dst_start + i.length for i in self.entries if i.dst_start < i.src_start]
            optimal_entries.sort()
            optimal_src_range = [True]*optimal_entries[0]

        print(optimal_src_range)

        return optimal_src_range

    def __repr__(self):
        return f"{self.source}-to-{self.destination}: {self.entries}"


class Almanac():
    """Represent a complete almanac with data."""

    def __init__(self):
        """Construct the almanac."""
        self.seeds = []
        self.maps = []

    def determine_shortest_path(self):
        """Determine a list of possible seeds that leed to a shortest path."""
        #locationmap = self.maps[-1]
        #optimal_entries = [i.dst_start + i.length for i in locationmap.entries if i.dst_start < i.src_start]
        #optimal_entries.sort()
        #optimal_src_range = [i for i in range(0, optimal_entries[0])]
        destinationlist = []
        for map in self.maps[::-1]:
            self.seeds = map.shortest_path_to(self.seeds)

        return destinationlist

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

        # Calc the amount of seeds
        seedline = text.split('\n')[0]
        new_almanac.seeds = calc_seeds(seedline.split(':')[1].split(' ')[1:])

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
            # We add an entry to the sort functionmap we're processing if it does
            else:
                newmap.entries.append(MapEntry.from_line(line))
                    
        return new_almanac

    def __repr__(self):
        return f"{self.maps}"


def calc_seeds(seedlist):
    """Takes a list of all the seed numbers. Returns a list of seeds."""
    seeds = []
    biggest_seed = 0

    # We create an iterator so we can loop 2 at a time
    seed_iterator = iter(seedlist)
    for seed in seed_iterator:
        seedrange = int(next(seed_iterator))
        if int(seed) + seedrange > biggest_seed:
            biggest_seed = int(seed) + seedrange

    # We create a list as big as the amount of seeds, with all set to False
    seeds = [False]*biggest_seed

    # Now the other way around
    smallest_seed = biggest_seed
    seed_iterator = iter(seedlist)
    for seed in seed_iterator:
        seedrange = int(next(seed_iterator))
        if int(seed) < smallest_seed:
            smallest_seed = int(seed)

    for id, seed in enumerate(seeds):
        if id > smallest_seed:
            seeds[id] = True

    return seeds


def main():
    with open('input', 'r') as f:
        almanac = Almanac.from_text(f.read())

    print(almanac.seeds)
    #shortest_path_seeds = almanac.determine_shortest_path()

    # TODO na bovenstaande matchen welke seeds hier aan voldoen, en dan wat daarvan de kortste is

if __name__ == '__main__':
    main()
