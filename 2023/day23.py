import click
import sys
import pprint

from collections import defaultdict
from dataclasses import dataclass
from typing import List

sys.setrecursionlimit(150000)

VERBOSE = False


@dataclass
class Point:
    x: int = 0
    y: int = 0


@dataclass
class Room:
    id: int = 0
    paths: List = None

    def __init__(self, id):
        self.id = id
        self.paths = []


@dataclass
class Path:
    dest: Room = None
    weight: int = 1
    exit: bool = False

    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = weight


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

    rv = {}

    y = 0
    for line in inp:
        x = 0
        for char in line:
            rv[(x, y)] = char
            x += 1
        y += 1
    maxx, maxy = x, y

    # start in 1,1 and start building out the tree based
    # x, y = 1, 0

    return rv, Point(maxx, maxy)


def validDest(mp, loc: Point, dest: Point, dry: bool):
    char = mp[(dest.x, dest.y)]
    if char == "#":
        return False
    elif char == "." or dry:
        return True
    elif char == ">":
        return True if dest.x > loc.x else False
    elif char == "<":
        return True if dest.x < loc.x else False
    elif char == "v":
        return True if dest.y > loc.y else False
    elif char == "^":
        return True if dest.y < loc.y else False
    return False


def neighbors(mp, size: Point, loc: Point, dry: bool):
    return map(
        lambda p: Point(p[0], p[1]),
        filter(
            lambda p: p[0] >= 0
            and p[1] >= 0
            and p[0] < size.x
            and p[1] < size.y
            and validDest(mp, loc, Point(p[0], p[1]), dry),
            [
                # NSEW only
                # (loc.x - 1, loc.y - 1),
                (loc.x - 1, loc.y),
                # (loc.x - 1, loc.y + 1),
                (loc.x, loc.y - 1),
                (loc.x, loc.y + 1),
                # (loc.x + 1, loc.y - 1),
                (loc.x + 1, loc.y),
                # (loc.x + 1, loc.y + 1),
            ],
        ),
    )


def longestHike(mp, size: Point, seen: set, loc: Point, dry: bool = False):
    # Base case, we hit the end
    if loc.x == size.x - 2 and loc.y == size.y - 1:
        return 0

    # Return longest hike from loc, avoiding seen, by doing a search, but
    # if we don't reach the exit then we need to abort
    hikes = []
    for n in neighbors(mp, size, loc, dry):
        if (n.x, n.y) in seen:
            continue
        scopy = seen.copy()
        scopy.add((n.x, n.y))
        lhike = longestHike(mp, size, scopy, n, dry)
        if lhike is not None:
            hikes.append(1 + lhike)
    # if hikes:
    # log("Hike from", loc, "longest are", hikes)
    return max(hikes) if hikes else None


def part1(inp):
    mp, size = inp
    return longestHike(mp, size, set((1, 0)), Point(1, 0), dry=False)


def chase(mp, size, loc, seen):
    # follow a tunnel to its end, return how long it was and the
    # coordinates of the branching room
    ct, lp = 0, loc
    n = list(filter(lambda x: (x.x, x.y) not in seen, neighbors(mp, size, lp, True)))
    seen.add((lp.x, lp.y))
    while len(n) == 1:
        ct += 1
        lp = n[0]
        seen.add((lp.x, lp.y))
        n = list(
            filter(lambda x: (x.x, x.y) not in seen, neighbors(mp, size, lp, True))
        )
    if len(n) == 0:
        return ct, lp
        log(lp)
        raise Exception("fuck?")
    return ct, lp


def toGraph(mp, size, loc, rv, seen):
    trials = [loc]

    while trials:
        loc = trials.pop(0)

        # now if this room doesn't exist, create it
        if (loc.x, loc.y) not in rv:
            rv[(loc.x, loc.y)] = Room(loc.y * size.x + loc.x)
        rm: Room = rv[(loc.x, loc.y)]

        # now get the neighbors from here that we should start chasing, chase
        # them, then install the doors
        for n in filter(
            lambda x: (x.x, x.y) not in seen, neighbors(mp, size, loc, True)
        ):
            # prevent us from backtracking from here
            seen.add((loc.x, loc.y))
            nweight, nloc = chase(mp, size, n, seen)
            seen.remove((loc.x, loc.y))
            if (nloc.x, nloc.y) not in rv:
                rv[(nloc.x, nloc.y)] = Room(nloc.y * size.x + nloc.x)
            rm.paths.append(Path(rv[(nloc.x, nloc.y)], nweight))

            # now see about adding this to skim later
            trials.append(nloc)

    pprint.pprint(rv)


def toGraph2(mp, size, loc, rv, seen):
    # rv is (x,y) -> Room and is shared with all recursive calls
    # convert map to a graph with weighted edges
    if (loc.x, loc.y) in seen:
        return

    seen.add((loc.x, loc.y))

    cur: Room = rv[(loc.x, loc.y)]
    wt, nbors = 1, list(neighbors(mp, size, loc, True))
    lx, ly = loc.x, loc.y
    while nbors:
        # if we have 1 neighbor, simply increment the path that we're
        # heading down
        if len(nbors) == 1:
            wt += 1
            lx, ly = nbor[0].x, nbor[0].y
            seen.add((lx, ly))
            nbors = list(neighbors(mp, size, Point(lx, ly), True))
            continue

        # the point we're at is going to be a new room, so let's set
        # and insert it
        rv[(lx, ly)] = Room(ly * size.x + lx)

        # if we have more than one, recurse and measure this path
        # and store it on both sides of the paths we just got so we
        # can walk the graph later
        for nbor in nbors:
            scopy = seen.copy()
            toGraph(mp, size, nbor, rv, scopy)

    # if we get here, that means there are no neighbors down this path
    # which might mean it's a dead end? see if end
    if loc.x == size.x - 2 and loc.y == size.y - 1:
        # add this segment and mark it
        dr = Path(None)
        dr.exit = True
        dr.weight = wt
        cur.paths.append(dr)


def part2(inp):
    mp, size = inp

    rv, seen = {}, set([(1, 0)])
    start_wt, loc = chase(mp, size, Point(1, 0), seen)
    toGraph(mp, size, loc, rv, seen)


def part2x(inp):
    mp, size = inp

    # these are long tunnels so let's see if we can just turn it into a tree
    tr, id, seen = [], 0, {}

    # init
    start = [0, 1, Point(1, 0), []]
    tr.append([start, list(neighbors(mp, size, Point(1, 0), True))])

    while tr:
        log("--", tr[0])
        src, neighborhood = tr[0]
        if (src[2].x, src[2].y) in seen:
            tr.pop(0)
            continue
        seen[(src[2].x, src[2].y)] = src

        # base case? TODO?
        if src[2].x == size.x - 2 and src[2].y == size.y - 1:
            raise Exception("base")

        # if we have no neighbors here, we need to populate
        if len(neighborhood) == 0:
            neighborhood = list(
                filter(
                    lambda p: (p.x, p.y) not in seen,
                    neighbors(mp, size, src[2], True),
                )
            )

        # if the neighborhood is a single element, we will continue from here
        while len(neighborhood) == 1:
            # increase length of taking this path then refresh neighbors from it
            # and try again
            seen[(neighborhood[0].x, neighborhood[0].y)] = True
            src[1] += 1
            neighborhood = list(
                filter(
                    lambda p: (p.x, p.y) not in seen,
                    neighbors(mp, size, neighborhood[0], True),
                )
            )

        # now neigborhood is 0 then discard this path by marking its weight
        # as none and move on
        if len(neighborhood) == 0:
            src[1] = None
            seen[(src[2].x, src[2].y)] = True
            tr.pop(0)
            continue

        # more than one neighbor, add them to the test list
        for n in neighborhood:
            id += 1
            nb = [id, 1, Point(n.x, n.y), []]
            src[3].append(nb)
            tr.append([nb, []])

    pprint.pprint(start)
    # log(start)


if __name__ == "__main__":
    main()
