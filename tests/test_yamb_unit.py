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
    def test_keep(self):
        for keepers in self.keep_hands:
            hand = y.Hand()
            hand.keep = keepers
            assert all((x.keep == i for x, i in zip(hand.dice, keepers)))

    def test_roll(self):
        for keepers in self.keep_hands[0:1]:
            hand = y.Hand()
            hand.keep = keepers
            hand.roll()
            assert all((not hasattr(x,"value") == i for x, i in zip(hand.dice,keepers)))
