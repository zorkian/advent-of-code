import click
import collections
import sys

VERBOSE = False


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
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    cards = {}
    for line in inp:
        card, rest = line.split(":")
        cardno = int(card.split(" ")[-1])

        win, have = rest.split(" | ", 2)
        win = set([int(n) if n else None for n in win.split(" ")])
        if None in win:
            win.remove(None)
        have = set([int(n) if n else None for n in have.split(" ")])
        if None in have:
            have.remove(None)

        cards[cardno] = [win, have]
    return cards


def part1(inp):
    rv = 0
    for cardno in inp.keys():
        ctr = 0
        win, have = inp[cardno]
        for idx in have:
            if idx in win:
                if ctr == 0:
                    ctr += 1
                else:
                    ctr *= 2
        rv += ctr
    return rv


def part2(inp):
    rv = 0

    wins = collections.defaultdict(int)
    for cardno in range(max(inp.keys())):
        cno = cardno + 1
        win, have = inp[cno]

        # Get as many copies as we have accumulated + of course this one
        # card we just pulled
        ct = wins[cno] + 1

        # Now see how many copies this card wins
        winners = len(have) - len(have - win)

        # Now add increments to those
        for idx in range(winners):
            wins[cno + idx + 1] += ct

    return sum(wins.values()) + len(wins)


if __name__ == "__main__":
    main()
