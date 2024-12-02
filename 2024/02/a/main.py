#!/usr/bin/env python

class Report():
    def __init__(self, levels):
        self.levels = [int(level.strip()) for level in levels]
        self.incrementing = self.levels[1] > self.levels[0]

    def is_safe(self):
        for id, level in enumerate(self.levels):
            prevlevel = self.levels[id-1]
            if id == 0:
                continue

            if self.incrementing:
                if prevlevel > level:
                    return False
            else:
                if prevlevel < level:
                    return False

            if level == prevlevel:
                return False
            if abs(level - prevlevel) > 3:
                return False

        return True


def main():

    reports = []

    with open('input', 'r') as f:
        for line in f.readlines():
            report = line.split(' ')
            reports.append(Report(report))

    print(
        len(
            [i for i in reports if i.is_safe()]
        )
    )


if __name__ == '__main__':
    main()
