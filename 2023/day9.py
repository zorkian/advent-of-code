import click
import numpy
import sys

from collections import defaultdict

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
    return [list(map(int, ln.split())) for ln in inp]
    return inp


def reduc(points):
    log(points)
    if not any(points):
        return 0

    return points[-1] + reduc(
        [points[idx + 1] - points[idx] for idx in range(len(points) - 1)]
    )


def reduc2(points):
    if not any(points):
        return 0

    rv = points[0] - reduc2(
        [points[idx + 1] - points[idx] for idx in range(len(points) - 1)]
    )
    log(rv, points)
    return rv


def part1(inp):
    rv = 0

    for cv in inp:
        rv += reduc(cv)

        # points = []
        # for idx in range(len(cv)):
        #    points.append((idx, cv[idx]))
        # points = numpy.array(points)
        # z = numpy.polyfit(points[:, 0], points[:, 1], 5)
        # f = numpy.poly1d(z)
        # rv += round(f(len(cv)))

    return rv


def part2(inp):
    rv = 0
    for cv in inp:
        rv += reduc2(cv)
    return rv


if __name__ == "__main__":
    main()
