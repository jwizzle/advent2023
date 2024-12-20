#!/usr/bin/env python


class Sector():

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        if self.content:
            return str(self.content.id)
        else:
            return '.'


class Block():

    def __init__(self, startpos, size):
        self.startpos = startpos
        self.size = size

    def __repr__(self):
        return str('.')


class File(Block):

    def __init__(self, id, startpos, size):
        self.startpos = startpos
        self.size = size
        self.id = id

    def __repr__(self):
        return str(self.id)


class DiskMap():

    def __init__(self, blocks):
        self.blocks = blocks
        self.sectors = []

    def fill_sectors(self):
        for block in self.blocks:
            for sector in range(1, block.size+1):
                sector = sector
                if isinstance(block, File):
                    self.sectors.append(Sector(content=block))
                else:
                    self.sectors.append(Sector())

    def find_free_sector(self):
        for id, sector in enumerate(self.sectors):
            if not sector.content:
                return id
        return 1  # This should never happen but makes my linter happy

    def defrag(self):
        for id, sector in reversed(list(enumerate(self.sectors))):
            free_sector_id = self.find_free_sector()
            if free_sector_id >= id:
                return self.sectors
            else:
                self.sectors[free_sector_id].content = sector.content
                self.sectors[id].content = None

    def checksum(self):
        total = 0
        for id, sector in enumerate(self.sectors):
            if sector.content:
                total += id * sector.content.id

        return total

    @classmethod
    def from_file(cls):
        blocks = []
        isfile = True
        startpos = 0
        file_id = 0

        with open('input', 'r') as f:
            for line in f.readlines():
                for char in line.strip():
                    size = int(char)
                    if isfile:
                        blocks.append(File(file_id, startpos, size))
                        file_id += 1
                    else:
                        blocks.append(Block(startpos, size))

                    isfile = not isfile
                    startpos += size

        return cls(
            blocks
        )

    def __repr__(self):
        return str(self.sectors)


def main():
    map = DiskMap.from_file()
    map.fill_sectors()
    map.defrag()
    print(map.checksum())


if __name__ == '__main__':
    main()
