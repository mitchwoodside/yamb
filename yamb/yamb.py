from random import randint
from operator import methodcaller


class Die:
    def __init__(self):
        self.keep = False

    def roll(self):
        self.value = randint(1, 6)


class Hand:
    dice_range = range(1, 6)

    def __init__(self):
        self.dice = [Die() for i in self.dice_range]
        self.keep = [0] * len(self.dice)
        self.rolls = 0

    @property
    def values(self):
        return [d.value for d in self.dice]

    @property
    def keep(self):
        return [d.keep for d in self.dice]

    @keep.setter
    def keep(self, keep):
        for i, die in enumerate(self.dice):
            die.keep = keep[i]

    def roll(self):
        self.rolls += 1
        for d in self.dice:
            if not d.keep:
                d.roll()
        return self.values

    def total(self):
        return sum(self.values)

    def yamb(self, display=False):
        if len(set(self.values)) == 1:
            return 50 + sum(self.values)
        else:
            return "X" if display else 0

    def ful(self, display=False):
        dice_set = set(self.values)
        if len(dice_set) == 2 and any(
            [
                self.values.count(self.values[0]) == 2,
                self.values.count(self.values[0]) == 3,
            ]
        ):
            return 30 + sum(self.values)
        else:
            return "X" if display else 0

    def kare(self, display=False):
        dice_set = set(self.values)
        if len(dice_set) == 2 and any(
            [
                self.values.count(self.values[0]) == 1,
                self.values.count(self.values[0]) == 4,
            ]
        ):
            return 40 + sum(
                4 * dice_set[0]
                if self.values.count(list(dice_set[0])) == 4
                else 4 * dice_set[1]
            )
        else:
            return "X" if display else 0

    def kenta(self, display=False):
        score = {1: 66, 2: 56, 3: 46}
        if sorted(self.values) in [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]] and self.rolls < 4:
            return score[self.rolls]
        else:
            return "X" if display else 0

    def count_value(self, number, display=False):
        count = self.values.count(number)
        return "X" if display and not count else count * number


class Column(list):
    score_methods = [
        methodcaller("count_value", 1),
        methodcaller("count_value", 2),
        methodcaller("count_value", 3),
        methodcaller("count_value", 4),
        methodcaller("count_value", 5),
        methodcaller("count_value", 6),
        methodcaller("total"),
        methodcaller("total"),
        methodcaller("kenta"),
        methodcaller("ful"),
        methodcaller("kare"),
        methodcaller("yamb"),
    ]
    display_methods = [
        methodcaller("count_value", 1, display=True),
        methodcaller("count_value", 2, display=True),
        methodcaller("count_value", 3, display=True),
        methodcaller("count_value", 4, display=True),
        methodcaller("count_value", 5, display=True),
        methodcaller("count_value", 6, display=True),
        methodcaller("total"),
        methodcaller("total"),
        methodcaller("kenta", display=True),
        methodcaller("ful", display=True),
        methodcaller("kare", display=True),
        methodcaller("yamb", display=True),
    ]

    def pad(self, size, fillvalue=None):
        return self + [fillvalue] * (size - len(self))

    def ordered(self):
        return self.pad(len(self.score_methods))

    def raw_scores(self, display=False):
        methods = self.display_methods if display else self.score_methods
        return [
            method(hand) if hand is not None else "" if display else 0
            for method, hand in zip(methods, self.ordered(),)
        ]

    @property
    def counts(self):
        return sum(self.raw_scores()[:6])

    @property
    def bonus(self):
        return 30 if self.counts >= 60 else 0

    @property
    def difference(self):
        return self.raw_scores()[0] * (self.raw_scores()[6] - self.raw_scores()[7])

    @property
    def specials(self):
        return sum(self.raw_scores()[8:])

    def scores(self, display=False):
        scores = self.raw_scores(display=display)
        scores.insert(6, self.counts + self.bonus)
        scores.insert(
            9,
            "-"
            if len(self) < 8 or not all((self[0], self[6], self[7]))
            else self.difference,
        )
        scores.append(self.specials if len(self) == 14 else "-")
        return scores


class Up(Column):
    def ordered(self):
        yamb_to_one = super().ordered()
        yamb_to_one.reverse()
        return yamb_to_one


class Free(Column):
    def __init__(self):
        for i, _ in enumerate(self.score_methods):
            self.append(None)


class Najava(Free):
    def __setitem__(self, index, hand):
        if hand.rolls < 2:
            super().__setitem__(index, hand)
        else:
            raise ValueError("cannot Najaviti after first roll")


class Card:
    column_labels = ("igra", "down", "free", "up", "najava")
    labels = (
        "ones",
        "twos",
        "threes",
        "fours",
        "fives",
        "sixes",
        "bonus",
        "max",
        "min",
        "difference",
        "straight",
        "full-house",
        "four-of-a-kind",
        "yamb",
        "specials",
    )
    print_template = "{:>14}|{:>4}|{:>4}|{:>4}|{:>6}"

    def __init__(self):
        self.columns = [Column(), Free(), Up(), Najava()]

    def print(self):
        print(self.print_template.format(*self.column_labels))
        for i in self.scores(display=True):
            print(self.print_template.format(*i))

    def scores(self, display=False):
        return [
            (a, b, c, d, e)
            for a, b, c, d, e in zip(
                self.labels, *[i.scores(display=display) for i in self.columns]
            )
        ]
