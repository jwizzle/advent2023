#!/usr/bin/env python

class OrderingRule():

    def __init__(self, text):
        self.before = int(text.split('|')[0])
        self.after = int(text.split('|')[1])
        self.pages = [self.before, self.after]


class Page():

    def __init__(self, number):
        self.number = int(number)
        self.validated = False

    def __repr__(self):
        return str(self.number)


class Update():

    def __init__(self, text):
        self.pages = [Page(i) for i in text.split(',')]

    def prohibited_pages_after_current(self, pages, page_id, prohibited_pages):
        for page_after_current in pages[page_id:]:
            if page_after_current.number in prohibited_pages:
                return True
        return False

    def validate_pages(self, rules, pages):
        for id, page in enumerate(pages):
            earlier_pages = [
                rule.before for rule in rules if page.number == rule.after
            ]
            if self.prohibited_pages_after_current(pages, id, earlier_pages):
                page.validated = False
            else:
                page.validated = True

        return False not in [page.validated for page in pages]

    def fix_order(self, rules):
        invalid_pages = [page for page in self.pages if not page.validated]
        valid_pages = [page for page in self.pages if page.validated]

        for invalidpage in invalid_pages:
            for id in range(0, len(valid_pages)+1):
                tmppages = valid_pages[:]
                if id == len(valid_pages):
                    tmppages.append(invalidpage)
                else:
                    tmppages.insert(id, invalidpage)

                if self.validate_pages(rules, tmppages):
                    valid_pages = tmppages
                    break

        return valid_pages

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

    with open('input', 'r') as f:
        for line in f.readlines():
            if '|' in line:
                rules.append(OrderingRule(line))
            if ',' in line:
                updates.append(Update(line))

    out = 0
    for update in updates:
        if not update.validate_pages(rules, update.pages):
            update.pages = update.fix_order(rules)
            out = out + update.middle_number()

    print(out)


if __name__ == '__main__':
    main()
