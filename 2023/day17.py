import click
import sys

from collections import defaultdict
from dataclasses import dataclass
from queue import PriorityQueue

VERBOSE = False

RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3


def log(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


@dataclass
class Point:
    path: list
    x: int = 0
    y: int = 0
    heat: int = 0
    dirs: str = "nnn"


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

    x, y = 0, 0
    for line in inp:
        x = 0
        for char in line:
            rv[(x, y)] = int(char)
            x += 1
        y += 1

    return Point([], x, y), rv


def nodes_from(loc, size, map):
    nodes = []

    log("FROM:", loc)

    # can we left
    if loc.x > 0 and loc.dirs[0] != "R" and loc.dirs != "LLL":
        nx, ny, pth = loc.x - 1, loc.y, loc.path.copy()
        pth.append((nx, ny))
        nodes.append(Point(pth, nx, ny, loc.heat + map[(nx, ny)], "L" + loc.dirs[0:2]))

    # can we right
    if loc.x < size.x - 1 and loc.dirs[0] != "L" and loc.dirs != "RRR":
        nx, ny, pth = loc.x + 1, loc.y, loc.path.copy()
        pth.append((nx, ny))
        nodes.append(Point(pth, nx, ny, loc.heat + map[(nx, ny)], "R" + loc.dirs[0:2]))

    # can we up
    if loc.y > 0 and loc.dirs[0] != "D" and loc.dirs != "UUU":
        nx, ny, pth = loc.x, loc.y - 1, loc.path.copy()
        pth.append((nx, ny))
        nodes.append(Point(pth, nx, ny, loc.heat + map[(nx, ny)], "D" + loc.dirs[0:2]))

    # can we down
    if loc.y < size.y - 1 and loc.dirs[0] != "U" and loc.dirs != "DDD":
        nx, ny, pth = loc.x, loc.y + 1, loc.path.copy()
        pth.append((nx, ny))
        nodes.append(Point(pth, nx, ny, loc.heat + map[(nx, ny)], "U" + loc.dirs[0:2]))

    log("TO:", nodes)

    return nodes


def dirs_from(tup, size):
    dirs = []
    if tup[0] > 0:
        dirs.append("L")
    if tup[1] > 0:
        dirs.append("U")
    if tup[0] < size.x - 1:
        dirs.append("R")
    if tup[1] < size.y - 1:
        dirs.append("D")
    return dirs


def part1(inp):
    # dijkstra version because fuck it
    size, map = inp

    unvisited = {
        (tup[0], tup[1], dir): True for tup in map for dir in dirs_from(tup, size)
    }
    came_from = {}
    cost_so_far = {tup: sys.maxsize for tup in unvisited}
    lookups = {}
    last_from = set()

    for dir in ("D", "R"):
        came_from[(0, 0, dir)] = None
        cost_so_far[(0, 0, dir)] = 0
        lookups[(0, 0, dir)] = Point(
            [(0, 0)],
            dirs=dir + "nn",
        )

    log(cost_so_far)

    while unvisited:
        current = None
        for tup in unvisited:
            if current is None or cost_so_far[tup] < cost_so_far[current]:
                current = tup

        node = lookups[current]

        if node.x == 12 and node.y == 12:
            log(node)

        for next in nodes_from(node, size, map):
            # log(current, next)
            nexttup = (next.x, next.y, next.dirs[0])
            log(nexttup)
            new_cost = cost_so_far[current] + map[(next.x, next.y)]
            if new_cost < cost_so_far[nexttup]:
                # log(
                #    "replacing",
                #    (next.x, next.y),
                #    "with",
                #    new_cost,
                #    "<",
                #    cost_so_far.get((next.x, next.y), None),
                # )
                cost_so_far[nexttup] = new_cost
                came_from[nexttup] = current
                lookups[nexttup] = next

        # skip revisiting this
        del unvisited[current]

    log()

    for route in (
        lookups[(size.x - 1, size.y - 1, "D")],
        lookups[(size.x - 1, size.y - 1, "R")],
    ):
        log(route.heat)
        for y in range(size.y):
            line = ""
            for x in range(size.x):
                line += "*" if (x, y) in route.path else "."
            log(line)
        log()

    return 0  # cost_so_far  # [(size.x - 1, size.y - 1)]


def part1_astar(inp):
    size, map = inp

    def h(loc):
        # Heuristic is the manhattan distance to the exit
        return abs(size.x - loc.x) + abs(size.y - loc.y)

    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    lookups = {}
    last_from = set()

    for dir in ("D", "R"):
        frontier.put((0, 0, dir), 0)
        came_from[(0, 0, dir)] = None
        cost_so_far[(0, 0, dir)] = 0
        lookups[(0, 0, dir)] = Point(
            [(0, 0)],
            dirs=dir + "nn",
        )

    while not frontier.empty():
        current = frontier.get()
        node = lookups[current]

        if node.x == 12 and node.y == 12:
            log(node)

        if current[0] == size.x - 1 and current[1] == size.y - 1:
            last_from.add(current[2])
            if len(last_from) == 2:
                break

        for next in nodes_from(node, size, map):
            # log(current, next)
            nexttup = (next.x, next.y, next.dirs[0])
            new_cost = cost_so_far[current] + map[(next.x, next.y)]
            if nexttup not in cost_so_far or new_cost < cost_so_far[nexttup]:
                # log(
                #    "replacing",
                #    (next.x, next.y),
                #    "with",
                #    new_cost,
                #    "<",
                #    cost_so_far.get((next.x, next.y), None),
                # )
                cost_so_far[nexttup] = new_cost
                frontier.put(nexttup, new_cost + h(next))
                came_from[nexttup] = current
                lookups[nexttup] = next

    log()

    for route in (
        lookups[(size.x - 1, size.y - 1, "D")],
        lookups[(size.x - 1, size.y - 1, "R")],
    ):
        log(route.heat)
        for y in range(size.y):
            line = ""
            for x in range(size.x):
                line += "*" if (x, y) in route.path else "."
            log(line)
        log()

    return 0  # cost_so_far  # [(size.x - 1, size.y - 1)]


def part1x(inp):
    size, map = inp

    # appender that saves us effort
    tries = [(Point(0, 0, 0), "nnn", {})]

    def trymove(tl, xoff, yoff, dirs, dir, path):
        nx, ny = tl.x + xoff, tl.y + yoff
        if (nx, ny) in path:
            return
        if nx < 0 or ny < 0 or nx >= size.x or ny >= size.y:
            return
        if dir * 3 == dirs or dirs[0] == {"L": "R", "R": "L", "U": "D", "D": "U"}[dir]:
            return
        pth = path.copy()
        pth[(nx, ny)] = 1
        tries.append((Point(nx, ny, tl.heat + map[(nx, ny)]), dir + dirs[0:2], pth))

    # try to do a BFS but don't allow us to cover any square that we
    # have already entered (I think that overlapping yourself will
    # never result in a cooler path?)
    minHeat = None
    while tries:
        # base case, we're at the exit, count this minHeat and then
        # don't add further
        tl, dirs, path = tries.pop(0)
        # log(tl, len(tries))
        if tl.x == size.x - 1 and tl.y == size.y - 1:
            if minHeat is None:
                minHeat = tl.heat
            else:
                minHeat = min(minHeat, tl.heat)
            log("new min", minHeat)
            continue

        # see if we can go left from here (if the last direction
        # was not a right and there's no repeat)
        trymove(tl, -1, 0, dirs, "L", path)
        trymove(tl, 1, 0, dirs, "R", path)
        trymove(tl, 0, -1, dirs, "U", path)
        trymove(tl, 0, 1, dirs, "D", path)

    return 0


def part2(inp):
    rv = 0
    return rv


if __name__ == "__main__":
    main()
