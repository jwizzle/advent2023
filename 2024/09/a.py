#!/usr/bin/env python


class Sector():

    def __init__(self, startpos, blocks):
        self.startpos = startpos
        self.blocks = blocks


class File(Sector):

    def __init__(self, id):
        self.id = id


class DiskMap():

    def __init__(self, sectors):
        self.sectors = sectors

    @classmethod
    def from_file(cls):
        sectors = []
        isfile = True

        with open('input', 'r') as f:
            for line in f.readlines():
                for id, char in enumerate(line.strip()):
                    if isfile:
                        sectors.append(File(id))
                    else:
                        sectors.append(Sector(0, 1))

                    isfile = -isfile

        return cls(
            sectors
        )

    def __repr__(self):
        return self.sectors

def main():
    map = DiskMap.from_file()
    print(map)


if __name__ == '__main__':
    main()
