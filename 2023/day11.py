import click
import sys

from collections import defaultdict, namedtuple

VERBOSE = False

Point = namedtuple("Point", ["x", "y"])
World = namedtuple("World", ["width", "height"])


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

    world = {}
    has_y = defaultdict(bool)
    has_x = defaultdict(bool)

    y = 0
    for line in inp:
        x = 0
        for char in line:
            if char == "#":
                world[(x, y)] = Point(x, y)
                has_x[x] = True
                has_y[y] = True
            x += 1
        y += 1

    return (World(width=x, height=y), has_x, has_y, world)


def distances(galaxy, has_x, has_y, points, extra=1):
    rv = 0

    for to_galaxy in points.values():
        if to_galaxy == galaxy:
            continue

        from_x = min(galaxy.x, to_galaxy.x)
        to_x = max(galaxy.x, to_galaxy.x)
        for x in range(from_x, to_x):
            rv += 1
            if x not in has_x:
                rv += extra

        from_y = min(galaxy.y, to_galaxy.y)
        to_y = max(galaxy.y, to_galaxy.y)
        for y in range(from_y, to_y):
            rv += 1
            if y not in has_y:
                rv += extra

    return rv


def part1(inp):
    world, has_x, has_y, points = inp

    rv = 0

    for galaxy in points.values():
        rv += distances(galaxy, has_x, has_y, points)

    return int(rv / 2)


def part2(inp):
    world, has_x, has_y, points = inp

    rv = 0

    for galaxy in points.values():
        rv += distances(galaxy, has_x, has_y, points, extra=999999)

    return int(rv / 2)


if __name__ == "__main__":
    main()
