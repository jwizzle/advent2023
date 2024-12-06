#!/usr/bin/env python

class OrderingRule():

    def __init__(self, text):
        self.before = int(text.split('|')[0])
        self.after = int(text.split('|')[1])
        self.pages = [self.before, self.after]


class Page():

    def __init__(self, number):
        self.number = int(number)


class Update():

    def __init__(self, text):
        self.pages = [Page(i) for i in text.split(',')]

    def check_ok(self, rules):
        for id, page in enumerate(self.pages):
            earlier_pages = [
                rule.before for rule in rules if page.number == rule.after
            ]

            for page_after in self.pages[id:]:
                if page_after.number in earlier_pages:
                    return False

        return True

    def middle_number(self):
        middle = float(len(self.pages))/2
        if middle % 2 != 0:
            return self.pages[int(middle - .5)].number
        else:
            return (self.pages[int(middle)], self.pages[int(middle-1)].number)

    def __repr__(self):
        return ",".join([str(page.number) for page in self.pages])


def main():
    updates = []
    rules = []
    print(rules)

    with open('input', 'r') as f:
        for line in f.readlines():
            if '|' in line:
                rules.append(OrderingRule(line))
            if ',' in line:
                updates.append(Update(line))

    print(
        sum(
            [update.middle_number() for update in updates if update.check_ok(rules)]
        )
    )


if __name__ == '__main__':
    main()
