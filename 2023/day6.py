import click
import numpy
import sys

from collections import defaultdict
from typing import List, Tuple

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
    times: List[int] = list(map(int, inp[0].split()[1:]))
    distances: List[int] = list(map(int, inp[1].split()[1:]))
    return (times, distances)


def part1(inp: Tuple[List[int], List[int]]):
    vals: List[int] = []
    times, distances = inp
    for idx in range(len(times)):
        time, distance = times[idx], distances[idx]

        ct = 0
        for acceltime in range(time):
            covered = acceltime * (time - acceltime)
            if covered > distance:
                ct += 1
        vals.append(ct)

    return numpy.prod(vals)


def part2(inp):
    vals: List[int] = []

    time = int("".join(map(str, inp[0])))
    distance = int("".join(map(str, inp[1])))

    ct = 0
    for acceltime in range(time):
        covered = acceltime * (time - acceltime)
        if covered > distance:
            ct += 1
    vals.append(ct)

    return numpy.prod(vals)


if __name__ == "__main__":
    main()
