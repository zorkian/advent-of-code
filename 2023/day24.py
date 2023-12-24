import click
import sys

from collections import defaultdict
from dataclasses import dataclass

VERBOSE = False


@dataclass
class Point:
    x: int = 0
    y: int = 0
    z: int = 0


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
    prefix = "inputs/day" + sys.argv[0].split(".")[0][-2:] + "."
    with open(prefix + ("test" if test else "input")) as f:
        return [l.strip() for l in f.readlines()]


def munge_input(inp):
    """
    Convert the input lines into whatever structure we need to handle the
    problem of the day.
    """
    rv = []
    for line in inp:
        pos, vel = line.split(" @ ", 2)
        rv.append(
            [
                Point(*list(map(int, pos.split(", ", 3)))),
                Point(*list(map(int, vel.split(", ", 3)))),
            ]
        )
    return rv


def intersects(h1, h2, frm, to):
    BIG = 40000000000000000

    h1posA, h1vel = h1
    h1posB = Point(
        h1posA.x + (h1vel.x * BIG),
        h1posA.y + (h1vel.y * BIG),
        h1posA.z + (h1vel.z * BIG),
    )

    h2posA, h2vel = h2
    h2posB = Point(
        h2posA.x + (h2vel.x * BIG),
        h2posA.y + (h2vel.y * BIG),
        h2posA.z + (h2vel.z * BIG),
    )

    # intersection thanks wikipedia
    p1, p2, p3, p4 = h1posA, h1posB, h2posA, h2posB
    try:
        tval = ((p1.x - p3.x) * (p3.y - p4.y)) - ((p1.y - p3.y) * (p3.x - p4.x))
        tval = tval / (
            ((p1.x - p2.x) * (p3.y - p4.y)) - ((p1.y - p2.y) * (p3.x - p4.x))
        )
        uval = ((p1.x - p3.x) * (p1.y - p2.y)) - ((p1.y - p3.y) * (p1.x - p2.x))
        uval = uval / (
            ((p1.x - p2.x) * (p3.y - p4.y)) - ((p1.y - p2.y) * (p3.x - p4.x))
        )
    except ZeroDivisionError:
        # pray
        return False

    # intersection if within 0..1
    if not (uval > 0 and uval < 1 and tval > 0 and tval < 1):
        return False

    # set up final coords
    fx = p1.x + (tval * (p2.x - p1.x))
    fy = p1.y + (tval * (p2.y - p1.y))

    # if we're in the range...
    if fx >= frm and fx <= to and fy >= frm and fy <= to:
        return True
    return False


def part1(inp):
    rv = 0
    for i in range(len(inp)):
        for j in range(i + 1, len(inp)):
            if intersects(inp[i], inp[j], 200000000000000, 400000000000000):
                rv += 1
    return rv


def part2(inp):
    rv = 0
    return rv


if __name__ == "__main__":
    main()
