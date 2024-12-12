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
        self.sectors = []
        for block in self.blocks:
            for sector in range(1, block.size+1):
                sector = sector
                if isinstance(block, File):
                    self.sectors.append(Sector(content=block))
                else:
                    self.sectors.append(Sector())

    def find_free_block(self, size):
        for id, block in enumerate(self.blocks):
            if not isinstance(block, File) and block.size >= size:
                return id
        return False

    def move_file(self, file_id, block_id, file):
        block = self.blocks[block_id]

        self.blocks[block_id] = file
        self.blocks[file_id] = Block(file_id, file.size)

        if file.size < block.size:
            remaining_size = block.size - file.size
            newblock = Block(block_id + 1, remaining_size)
            self.blocks.insert(block_id + 1, newblock)
            return 1
        return 0

    def find_movable_file(self):
        for id, block in reversed(list(enumerate(self.blocks))):
            if isinstance(block, File):
                free_block_id = self.find_free_block(block.size)
                if free_block_id and free_block_id < id:
                    return id, block

        return False

    def defrag_byfile(self):
        movable_files = True
        while movable_files:
            result = self.find_movable_file()
            if result:
                id, file = result
                free_block_id = self.find_free_block(file.size)
                self.move_file(id, free_block_id, file)
            else:
                movable_files = False

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
                    startpos += 1

        return cls(
            blocks
        )

    def __repr__(self):
        return str(self.sectors)


def main():
    map = DiskMap.from_file()
    map.defrag_byfile()
    map.fill_sectors()
    print(map.checksum())


if __name__ == '__main__':
    main()
