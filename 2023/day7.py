import click
import sys

from collections import defaultdict
from typing import List, Dict

VERBOSE = False


class HandType:
    FIVE_KIND = 6
    FOUR_KIND = 5
    FULL_HOUSE = 4
    THREE_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0
    NONE = None


class Card:
    face = None

    def __init__(self, face):
        self.face = face
        self.order = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 11,
            "T": 10,
        }.get(self.face, None)

        self.order2 = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 1,
            "T": 10,
        }.get(self.face, None)

        if self.order is None:
            self.order = int(self.face)
        if self.order2 is None:
            self.order2 = int(self.face)

    def __repr__(self):
        return "%s(%d)" % (self.face, self.order)


class Hand(object):
    def __init__(self, line):
        cards, bid = line.split()

        self.bid = int(bid)
        self.cardList = cards
        self.cards = [Card(c) for c in cards]
        # self.cards.sort(key=lambda c: c.order, reverse=True)
        self.counts = defaultdict(int)
        for card in self.cards:
            self.counts[card.face] += 1
        self.score()
        self.score2()

    def score(self):
        self.handType = HandType.NONE

        # Get the card count values
        counts = list(self.counts.values())
        counts.sort(reverse=True)
        counts = "".join(map(str, counts))

        # Categorize the hand
        if len(self.counts) == 1:
            self.handType = HandType.FIVE_KIND
        elif len(self.counts) == 2:
            if counts == "41":
                self.handType = HandType.FOUR_KIND
            elif counts == "32":
                self.handType = HandType.FULL_HOUSE
        elif len(self.counts) == 3:
            if counts == "311":
                self.handType = HandType.THREE_KIND
            elif counts == "221":
                self.handType = HandType.TWO_PAIR
        elif len(self.counts) == 4:
            self.handType = HandType.ONE_PAIR
        elif len(self.counts) == 5:
            self.handType = HandType.HIGH_CARD

        if self.handType == HandType.NONE:
            raise Exception("no handtype for %s" % (self.cards,))

    def score2(self):
        self.handType2 = HandType.NONE

        # Get the card count values
        counts = list(self.counts.values())
        counts.sort(reverse=True)
        counts = "".join(map(str, counts))

        # If no jokers, just use score1 and return
        if self.counts["J"] == 0:
            self.handType2 = self.handType

        # If one joker
        elif self.counts["J"] == 1:
            if len(self.counts) == 2:
                if counts == "41":
                    self.handType2 = HandType.FIVE_KIND
            elif len(self.counts) == 3:
                if counts == "311":
                    self.handType2 = HandType.FOUR_KIND
                elif counts == "221":
                    self.handType2 = HandType.FULL_HOUSE
            elif len(self.counts) == 4:
                self.handType2 = HandType.THREE_KIND
            elif len(self.counts) == 5:
                self.handType2 = HandType.ONE_PAIR

        # If two jokers
        elif self.counts["J"] == 2:
            if len(self.counts) == 2:
                if counts == "32":
                    self.handType2 = HandType.FIVE_KIND
            elif len(self.counts) == 3:
                if counts == "221":
                    self.handType2 = HandType.FOUR_KIND
            elif len(self.counts) == 4:
                self.handType2 = HandType.THREE_KIND

        # If three
        elif self.counts["J"] == 3:
            if len(self.counts) == 2:
                if counts == "32":
                    self.handType2 = HandType.FIVE_KIND
            elif len(self.counts) == 3:
                if counts == "311":
                    self.handType2 = HandType.FOUR_KIND

        # If four or five
        elif self.counts["J"] in (4, 5):
            self.handType2 = HandType.FIVE_KIND

        if self.handType2 == HandType.NONE:
            raise Exception("no handtype for %s" % (self.cards,))

    def __repr__(self):
        return "[%s -- %s]" % (self.handType2, self.cardList)


def log(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


@click.command()
@click.option("-p1", is_flag=True, help="Run part 1.")
@click.option("-p2", is_flag=True, help="Run part 2.")
@click.option("-test", is_flag=True, help="Use test inputs.")
@click.option("-v", is_flag=True, help="Print verbosely.")
def main(p1, p2, test, v):
    global VERBOSE
    VERBOSE = v
    log("p1 =", p1, "|| p2 =", p2, "|| test =", test, "|| v =", v)
    inp = munge_input(load_input(test))
    log("Munged input:", inp, "\n")
    print(part1(inp) if p1 else part2(inp))


def load_input(test):
    prefix = "inputs/day" + sys.argv[0].split(".")[0][-1] + "."
    with open(prefix + ("test" if test else "input")) as f:
        return [l.strip() for l in f.readlines()]


def munge_input(inp):
    """
    Convert the input lines into whatever structure we need to handle the
    problem of the day.
    """
    return [Hand(line) for line in inp]


def part1(inp):
    inp.sort(key=lambda hand: [hand.handType, [c.order for c in hand.cards]])

    rv = 0
    for idx in range(len(inp)):
        rv += (idx + 1) * inp[idx].bid

    return rv


def part2(inp):
    inp.sort(key=lambda hand: [hand.handType2, [c.order2 for c in hand.cards]])
    log(inp)

    rv = 0
    for idx in range(len(inp)):
        rv += (idx + 1) * inp[idx].bid

    return rv


if __name__ == "__main__":
    main()
