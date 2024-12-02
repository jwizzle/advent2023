#!/usr/bin/env python

class Report():
    def __init__(self, levels, tolerating=False):
        self.levels = [int(str(level).strip()) for level in levels]
        self.incrementing = self.levels[1] > self.levels[0]
        self.tolerating = tolerating

    @classmethod
    def without_levelid(cls, levels, levelid):
        return cls(
            [level for id, level in enumerate(levels) if id != levelid],
            tolerating=True
        )

    def check_rules(self, level, prevlevel):
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

    def check_tolerated(self):
        for id, level in enumerate(self.levels):
            newreport = Report.without_levelid(self.levels, id)
            if newreport.check_safety():
                return True

        return False

    def check_safety(self):
        isvalid = True

        for id, level in enumerate(self.levels):
            prevlevel = self.levels[id-1]
            if id == 0:
                continue

            if not self.check_rules(level, prevlevel):
                isvalid = False

        if not isvalid and not self.tolerating:
            return self.check_tolerated()
        else:
            return isvalid


def main():
    reports = []

    with open('input', 'r') as f:
        for line in f.readlines():
            report = line.split(' ')
            reports.append(Report(report))

    print(
        len(
            [i for i in reports if i.check_safety()]
        )
    )


if __name__ == '__main__':
    main()
