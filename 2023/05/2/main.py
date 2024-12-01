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

    def get_src(self, input):
        """Get the source needed for a given destination."""
        for entry in self.entries:
            last_num = entry.dst_start + entry.length - 1

            if input <= last_num and input >= entry.dst_start:
                diff = input - entry.dst_start
                return entry.src_start + diff

        return input

    def __repr__(self):
        return f"{self.source}-to-{self.destination}: {self.entries}"


class Almanac():
    """Represent a complete almanac with data."""

    def __init__(self):
        """Construct the almanac."""
        self.seeds = []
        self.maps = []

    def determine_shortest_path(self):
        """Determine which closest location corresponds to an existing seed.
        
        We walk through our maps backwards starting at location 0. If a
        valid seed is found from the given ranges, then we return it since
        it's the closest.
        """
        seedfound = False
        curloc = 0

        while not seedfound:
            resolved_src = curloc

            for map in self.maps[::-1]:
                resolved_src = map.get_src(resolved_src)

            if self.match_seed(resolved_src):
                return curloc

            curloc += 1

        return curloc

    @classmethod
    def from_text(cls, text):
        """Generate a complete almanac from our input."""
        new_almanac = cls()
        seedline = text.split('\n')[0]
        new_almanac.seeds = seedline.split(':')[1].split(' ')[1:]

        for line in text.split('\n')[2:]:
            if not line:
                new_almanac.maps.append(newmap)
                continue

            if not line[0].isdigit():
                src_dst = line.split(' ')[0].split('-to-')
                newmap = Map(src_dst[0], src_dst[1])
            else:
                newmap.entries.append(MapEntry.from_line(line))
                    
        return new_almanac

    def __repr__(self):
        return f"{self.maps}"

    def match_seed(self, seed):
        """Check if there is a matching start seed for the given seed."""
        seed_iterator = iter(self.seeds)
        for seed_in_list in seed_iterator:
            seedrange = int(next(seed_iterator))
            if seed >= int(seed_in_list) and seed <= int(seed_in_list) + seedrange:
                return True

        return False

def main():
    with open('input', 'r') as f:
        text = f.read()
        almanac = Almanac.from_text(text)

    print(almanac.determine_shortest_path())

if __name__ == '__main__':
    main()
