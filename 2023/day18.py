import click
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
    prefix = "inputs/day" + sys.argv[0].split(".")[0][-2:] + "."
    with open(prefix + ("test" if test else "input")) as f:
        return [l.strip() for l in f.readlines()]


def munge_input(inp):
    """
    Convert the input lines into whatever structure we need to handle the
    problem of the day.
    """
    # R 6 (#70c710)

    rv = []
    for line in inp:
        dir, length, color = line.split()
        rv.append((dir, int(length), color[2:-1]))

    return rv


def neighbors(x, y):
    return [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]


def bfs(map, x, y, minx, maxx, miny, maxy):
    counts = {(x, y): 1}
    tries = [(x, y)]

    while tries:
        next = tries.pop(0)

        # get neighbors, ignore if we hit a wall
        for x, y in neighbors(next[0], next[1]):
            if x < minx or x > maxx or y < miny or y > maxy:
                continue
            if map.get((x, y), None) is not None:
                continue
            if (x, y) in counts:
                continue
            tries.append((x, y))
            counts[(x, y)] = 1

    return len(counts.keys())


def part1(inp):
    map = {}
    x, y, dug = 0, 0, 0
    minx, miny, maxx, maxy = sys.maxsize, sys.maxsize, 0, 0

    for move in inp:
        dir, length, color = move
        dug += length
        log("!!", dir, length, ">>", x, y, color)
        if dir == "U":
            for i in range(y - length, y):
                map[(x, i)] = color
                log((i, y))
                y -= 1
        elif dir == "D":
            for i in range(y + 1, y + length + 1):
                map[(x, i)] = color
                log((i, y))
                y += 1
        elif dir == "L":
            for i in range(x - length, x):
                map[(i, y)] = color
                log((i, y))
                x -= 1
        elif dir == "R":
            for i in range(x + 1, x + length + 1):
                map[(i, y)] = color
                log((i, y))
                x += 1
        log(dir, length, ">>", x, y, color)
        minx, miny = min(minx, x), min(miny, y)
        maxx, maxy = max(maxx, x), max(maxy, y)

    # now print the map
    for y in range(miny, maxy + 1):
        line = ""
        for x in range(minx, maxx + 1):
            color = map.get((x, y), ".00000")
            line += color[0]
        log(line)

    log(minx, maxx, miny, maxy)

    return dug + bfs(map, 1, 1, minx, maxx, miny, maxy)


def part2(inp):
    map = {}
    x, y, dug = 0, 0, 0
    minx, miny, maxx, maxy = sys.maxsize, sys.maxsize, 0, 0
    vertices = []

    for move in inp:
        dir, length, color = move

        dir = {"0": "R", "1": "D", "2": "L", "3": "U"}[color[-1]]
        length = int(color[0:5], base=16)

        dug += length
        log("!!", dir, length, ">>", x, y, color)
        if dir == "U":
            y -= length
        elif dir == "D":
            y += length
        elif dir == "L":
            x -= length
        elif dir == "R":
            x += length
        vertices.append((x, y))
        minx, miny = min(minx, x), min(miny, y)
        maxx, maxy = max(maxx, x), max(maxy, y)

    # x/y must be 0
    assert (x, y) == (0, 0), "didn't return"

    # do vertex math thanks google
    total = 0
    for idx in range(len(vertices)):
        x1, y1 = vertices[idx]
        x2, y2 = vertices[(idx + 1) % len(vertices)]
        total += (x1 * y2) - (y1 * x2)
    log(dug, vertices)

    # no idea why I have to add 1
    return int(abs(total / 2) + (dug / 2)) + 1


if __name__ == "__main__":
    main()
