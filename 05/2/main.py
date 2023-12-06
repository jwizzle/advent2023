#!/usr/bin/env python3

class MapEntry():
    """Represent a single entry in a map."""

    def __init__(self, dst_start, src_start, length):
        """Construct the entry."""
        self.dst_start = int(dst_start)
        self.src_start = int(src_start)
        self.length = int(length)

    def src_from_dst(self, dst):
        """Get a matching src for a dst in this range."""
        last_num = self.dst_start + self.length - 1

        if dst <= last_num and dst >= self.dst_start:
            diff = dst - self.dst_start
            return self.src_start + diff
        else:
            return dst

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

    def get_src(self, input):
        """Get the source needed for a given destination."""
        for entry in self.entries:
            last_num = entry.dst_start + entry.length - 1

            if input <= last_num and input >= entry.dst_start:
                diff = input - entry.dst_start
                return entry.src_start + diff

        # If we reach this the input is not mapped
        return input

    def shortest_path_to(self, seedmap):
        """Find the shortest paths to entries in a given seedmap.

        Seein entries in the seedmap as destinations to find.
        Returns a new seedmap with sources of this map is the new seeds.
        """
        new_seedmap = []

        if seedmap:
            #new_seedmap = {self.get_src(dest): seedmap[dest] for dest in seedmap}
            new_seedmap = [(self.get_src(dest), loc) for dest, loc in seedmap]
        # This is probably the location map
        # so we kickstart this whole thing by making a seedmap
        # consisting of 0 -> the end of range of lowest mapentry
        # 0 -> 60 in the examples.
        else:
            optimal_entries = [i.dst_start + i.length for i in self.entries if i.dst_start < i.src_start]
            optimal_entries.sort()
            #new_seedmap = {self.get_src(id): id for id, dest in enumerate([None]*optimal_entries[0])}
            new_seedmap = [(self.get_src(id), id) for id, dest in enumerate([None]*optimal_entries[0])]

        return new_seedmap

    def __repr__(self):
        return f"{self.source}-to-{self.destination}: {self.entries}"


class Almanac():
    """Represent a complete almanac with data."""

    def __init__(self):
        """Construct the almanac."""
        self.seeds = []
        self.maps = []

    def determine_shortest_path(self):
        """Determine a map of seeds and the shortest location they might lead to."""
        seedmap = []
        for map in self.maps[::-1]:
            seedmap = map.shortest_path_to(seedmap)

        return seedmap

    @classmethod
    def from_text(cls, text):
        """Generate a complete almanac from our input."""
        new_almanac = cls()

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


def match_seed(pathmap, furthest_location, seedlist):
    """Takes a list of all the seed numbers. Returns a list of seeds."""
    closest_location = furthest_location
    seed_sets = []

    # We create an iterator so we can loop 2 at a time
    seed_iterator = iter(seedlist)
    for seed in seed_iterator:
        seedrange = int(next(seed_iterator))
        seed_sets.append((int(seed), seedrange))

    for seed, loc in pathmap:
        intseed = int(seed)
        for start, length in seed_sets:
            if intseed >= start and intseed <= start+length:
                if loc < closest_location:
                    closest_location = loc

    return closest_location

def main():
    with open('input', 'r') as f:
        text = f.read()
        almanac = Almanac.from_text(text)

    shortest_path_map = almanac.determine_shortest_path()

    furthest_location = 0
    for seed, loc in shortest_path_map:
        if loc > furthest_location:
            furthest_location = loc

    seedline = text.split('\n')[0]
    print(match_seed(shortest_path_map, furthest_location, seedline.split(':')[1].split(' ')[1:]))

if __name__ == '__main__':
    main()
