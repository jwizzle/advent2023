#!/usr/bin/env python


class Plot():

    def __init__(self, row, pos, region):
        self.row = row
        self.pos = pos
        self.region_id = region
        self.neighbours = []
        self.fences = 0
        self.processed = False

    def generate_region(self, visited=[]):
        yield self
        for neighbour in self.neighbours:
            if (
                neighbour.region_id == self.region_id and
                neighbour not in visited
            ):
                yield from neighbour.generate_region(visited=visited+[self])

        return False

    def __repr__(self):
        return self.region_id


class Region():

    def __init__(self, id):
        self.id = id
        self.plots = []
        self.area = self.get_area
        self.perimiter = 0
        self.price = 0

    def update_price(self):
        self.price = self.perimiter * self.get_area()

    def update_perimiter(self):
        for plot in self.plots:
            perimiter = 4
            for neighbour in plot.neighbours:
                if neighbour.region_id == plot.region_id:
                    perimiter -= 1
            self.perimiter += perimiter

    def get_area(self):
        return len(self.plots)

    def __repr__(self):
        return str({
            self.id: self.plots
        })


class Garden():

    def __init__(self, matrix):
        self.matrix = matrix
        self.regions = []

    def update_prices(self):
        for region in self.regions:
            region.update_price()

    def update_perimiters(self):
        for region in self.regions:
            region.update_perimiter()

    def get_region(self, id):
        for region in self.regions:
            if region.id == id:
                return region
        return None

    def create_valid_regionid(self, letter, tried=""):
        tried = tried+letter
        if not self.get_region(tried):
            return tried
        else:
            return self.create_valid_regionid(letter, tried=tried)

    def create_regions(self):
        plots = [plot for row in self.matrix for plot in row]

        for plot in plots:
            if plot.processed:
                continue

            region_id = self.create_valid_regionid(plot.region_id)
            existregion = self.get_region(region_id)

            if not existregion:
                existregion = Region(region_id)
                self.regions.append(existregion)

            for regionplot in plot.generate_region():
                existregion.plots.append(regionplot)
                regionplot.processed = True
            existregion.plots = list(set(existregion.plots))

    def find_neighbours(self, plot):
        if plot.row - 1 >= 0:
            north = self.matrix[plot.row-1][plot.pos]
        else:
            north = None

        if plot.pos + 1 < len(self.matrix[0]):
            east = self.matrix[plot.row][plot.pos+1]
        else:
            east = None

        if plot.row + 1 < len(self.matrix):
            south = self.matrix[plot.row+1][plot.pos]
        else:
            south = None

        if plot.pos - 1 >= 0:
            west = self.matrix[plot.row][plot.pos-1]
        else:
            west = None

        return [north, east, south, west]

    def update_neighbours(self):
        for line in self.matrix:
            for plot in line:
                plot.neighbours = [i for i in self.find_neighbours(plot) if i]

    @classmethod
    def from_file(cls):
        matrix = []

        with open('input', 'r') as f:
            for row, line in enumerate(f.readlines()):
                newline = []
                for pos, char in enumerate(line.strip()):
                    newline.append(Plot(row, pos, char))

                matrix.append(newline)

        return cls(matrix)

    def __repr__(self):
        out = ""
        for line in self.matrix:
            for plot in line:
                out += str(plot)
            out += "\n"
        return out


def main():
    garden = Garden.from_file()
    garden.update_neighbours()
    print('neighbours updated')
    garden.create_regions()
    print('regions created')
    garden.update_perimiters()
    print('perimiters updated')
    garden.update_prices()

    print(garden.regions)
    print(sum([i.price for i in garden.regions]))


if __name__ == '__main__':
    main()
