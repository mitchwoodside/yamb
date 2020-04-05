from yamb import yamb as y


class TestDie:
    def test_roll(self):
        die = y.Die()
        rolls = []
        for i in range(1000):
            die.roll()
            rolls.append(die.value)
            assert type(rolls[-1]) == int
            assert rolls[-1] > 0 and rolls[-1] < 7
        for i in range(1, 7):
            assert rolls.count(i) in range(134, 200)


class TestHand:
    keep_hands = (
        (0, 0, 0, 0, 0),
        (1, 1, 0, 0, 0),
        (1, 0, 1, 0, 1),
    )

    @staticmethod
    def set_dice(hand, iterable):
        for i, die in enumerate(hand.dice):
            die.value = iterable[i]

    def keepers_kept(self, hand, keepers=(0, 0, 0, 0, 0)):
        hand.keep = keepers
        return all((x.keep == i for x, i in zip(hand.dice, keepers)))

    def rollers_rolled(self, hand, keepers=(0, 0, 0, 0, 0)):
        hand.keep = keepers
        hand.roll()
        return all((not bool(x.value) == i for x, i in zip(hand.dice, keepers)))

    def test_keep(self):
        for k in self.keep_hands:
            hand = y.Hand()
            assert self.keepers_kept(hand, k)

    def test_roll(self):
        for k in self.keep_hands:
            hand = y.Hand()
            assert self.rollers_rolled(hand, k)
            assert hand.rolls == 1

    def set_and_run(self, hand, iterable, method):
        self.set_dice(hand, iterable)
        return getattr(hand, method)()

    def evaluate_scores(self, *args):
        for dice, score, method in args:
            yield self.set_and_run(y.Hand(), dice, method) == score

    def test_scores(self):
        scores = (
            ((1, 2, 3, 4, 5), 15, "total"),
            ([2] * 5, 60, "yamb"),
            ((5, 5, 5, 5, 1), 0, "yamb"),
            ((1, 1, 1, 2, 2), 37, "ful"),
            ((1, 1, 2, 2, 3), 0, "ful"),
            ((4, 4, 4, 4, 6), 56, "kare"),
            ((4, 4, 4, 3, 3), 0, "kare"),
        )
        for i in self.evaluate_scores(*scores):
            assert i
