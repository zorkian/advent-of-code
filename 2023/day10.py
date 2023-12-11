import click
import sys

from collections import namedtuple

VERBOSE = False

Point = namedtuple("Point", ["x", "y"])


class Pipe:
    def __init__(self, x, y, p1, p2, start=False):
        self.x = x
        self.y = y
        self.p1 = p1
        self.p2 = p2
        self.start = start
        self.ctr = 0

    def inflate(self, pipes):
        if type(self.p1) == Point:
            if self.p1.y not in pipes:
                self.p1 = None
            elif self.p1.x not in pipes[self.p1.y]:
                self.p1 = None
            else:
                self.p1 = pipes[self.p1.y][self.p1.x]
                self.p1.adopt(self)

        if type(self.p2) == Point:
            if self.p2.y not in pipes:
                self.p2 = None
            elif self.p2.x not in pipes[self.p2.y]:
                self.p2 = None
            else:
                self.p2 = pipes[self.p2.y][self.p2.x]
                self.p2.adopt(self)

    def adopt(self, pipe):
        if self.start:
            if self.p2 is None:
                self.p2 = pipe
                return True
            else:
                raise Exception("fuck2")

        if type(self.p1) == Point and self.p1 == (pipe.x, pipe.y):
            self.p1 = pipe
            self.ctr = pipe.ctr + 1
            return True
        elif type(self.p2) == Point and self.p2 == (pipe.x, pipe.y):
            self.p2 = pipe
            self.ctr = pipe.ctr + 1
            return True
        return False

    def valid(self):
        if type(self.p1) == Point:
            self.p1 = None
        if type(self.p2) == Point:
            self.p2 = None

        if self.p1 is None or self.p2 is None:
            return False
        return True

    def beginAdoptions(self, pipes):
        # We are a starter, we need to look for the two people who point at us,
        # which we are guaranteed to have... then we set ourselves up to point to
        # them and we can resume the normal adoption process
        for offsets in (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            # (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ):
            tx = self.x + offsets[0]
            ty = self.y + offsets[1]
            if ty not in pipes or tx not in pipes[ty]:
                continue
            if pipes[ty][tx] and pipes[ty][tx].adopt(self):
                self.p1 = pipes[ty][tx]
                break

        # continue adopting down one of the paths until we get back to ourselves,
        # we arbitrarily start going down the p1 path
        curPipe = self.p1
        while curPipe != self:
            coords = curPipe.nextLocation()
            # log(curPipe.x, curPipe.y, coords)
            if not pipes[coords.y][coords.x].adopt(curPipe):
                raise Exception("fuck", curPipe.x, curPipe.y)
            else:
                if type(curPipe.p1) == Point:
                    curPipe.p1 = pipes[coords.y][coords.x]
                elif type(curPipe.p2) == Point:
                    curPipe.p2 = pipes[coords.y][coords.x]

            curPipe = pipes[coords.y][coords.x]

    def nextLocation(self):
        if type(self.p1) == Point:
            return self.p1
        elif type(self.p2) == Point:
            return self.p2


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
    # log("Munged input:", inp, "\n")
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

    start = (0, 0)
    y = 0
    for line in inp:
        rv[y] = {}
        x = 0
        for char in line:
            if char == "|":
                rv[y][x] = Pipe(x, y, Point(x, y - 1), Point(x, y + 1))
            elif char == "-":
                rv[y][x] = Pipe(x, y, Point(x - 1, y), Point(x + 1, y))
            elif char == "L":
                rv[y][x] = Pipe(x, y, Point(x + 1, y), Point(x, y - 1))
            elif char == "J":
                rv[y][x] = Pipe(x, y, Point(x - 1, y), Point(x, y - 1))
            elif char == "7":
                rv[y][x] = Pipe(x, y, Point(x - 1, y), Point(x, y + 1))
            elif char == "F":
                rv[y][x] = Pipe(x, y, Point(x + 1, y), Point(x, y + 1))
            elif char == "S":
                rv[y][x] = Pipe(x, y, None, None, start=True)
                start = Point(x, y)
            else:
                rv[y][x] = None
            x += 1
        y += 1
    size = (x, y)

    # log(rv)
    rv[start.y][start.x].beginAdoptions(rv)

    # now remove everything that isn't wired up
    for y in rv.keys():
        xk = list(rv[y].keys())
        for x in xk:
            if rv[y][x] and not rv[y][x].valid():
                rv[y][x] = None

    return (start, size, rv)


def part1(inp):
    start, size, pipes = inp

    pipe = pipes[start.y][start.x]
    return int((max(pipe.p1.ctr, pipe.p2.ctr) + 1) / 2)


def nextLoc(loc, size):
    # calculate next valid location
    x = loc.x + 1
    if x < size.x:
        return (x, loc.y)
    x = 0
    y = loc.y + 1
    if y < size.y:
        return Point(x, y)
    return None


def inOrOut(loc, size, pipes):
    # cast two lines, horizontal and vertical, divide the counts
    # based on "before" and "after" the location
    counts = []

    ctr = 0
    for y in range(size.y):
        if pipes[y][loc.x] and pipes[y][loc.x].valid():
            ctr += 1
        elif y == loc.y:
            counts.append(ctr)
            ctr = 0
    counts.append(ctr)
    ctr = 0

    hitWallV = True if counts[0] == 0 or counts[1] == 0 else False
    wasOddV = True if counts[0] % 2 == 1 and counts[1] % 2 == 1 else False

    counts = []
    for x in range(size.x):
        if pipes[loc.y][x] and pipes[loc.y][x].valid():
            ctr += 1
        elif x == loc.x:
            counts.append(ctr)
            ctr = 0
    counts.append(ctr)

    hitWallH = True if counts[0] == 0 or counts[1] == 0 else False
    wasOddH = True if counts[0] % 2 == 1 and counts[1] % 2 == 1 else False

    # if we hit a wall, we're not inside
    if hitWallH or hitWallV:
        return False

    # if we had odd pairs, we're inside
    return wasOddV or wasOddH


def coordsFromLoc(loc):
    return [
        Point(x=loc.x - 1, y=loc.y - 1),
        Point(x=loc.x, y=loc.y - 1),
        Point(x=loc.x + 1, y=loc.y - 1),
        Point(x=loc.x - 1, y=loc.y),
        Point(x=loc.x + 1, y=loc.y),
        Point(x=loc.x - 1, y=loc.y + 1),
        Point(x=loc.x, y=loc.y + 1),
        Point(x=loc.x + 1, y=loc.y + 1),
    ]


def paint(loc, size, tests, pipes):
    # if we've already determined, then skip
    # if loc.y in tests and loc[0] in tests[loc.y]:
    #    return (tests[loc.y][loc[0]], nextLoc(loc, size))

    # if this location is a pipe, move on
    if pipes[loc.y][loc.x]:
        if pipes[loc.y][loc.x].valid():
            return (False, nextLoc(loc, size))

    # not a pipe, cast a ray and see if this is in or out
    ioo = inOrOut(loc, size, pipes)
    if ioo:
        log(ioo, loc)
    # return (ioo, nextLoc(loc, size))

    # initialize
    tests[loc.y][loc.x] = ioo

    # flood fill
    tested = {}
    tested[loc] = True
    coords = coordsFromLoc(loc)
    while len(coords) > 0:
        coord = coords.pop(0)

        if coord in tested:
            continue
        if coord.x < 0 or coord.y < 0 or coord.x >= size.x or coord.y >= size.y:
            continue
        if tests[coord.y].get(coord.x, False):
            continue
        if pipes[coord.y][coord.x] and pipes[coord.y][coord.x].valid():
            continue

        tests[coord.y][coord.x] = ioo
        tested[coord] = True
        coords += coordsFromLoc(coord)

    # return
    return (ioo, nextLoc(loc, size))


def part2(inp):
    start, size, pipes = inp

    # start from corner, the logic we're going to use is that if there's an
    # odd number of pipes in any direction (horizontal or vertical) then we
    # are inside the loop. outside spaces are in zones that have an even count
    # of pipes on all sides.
    rv = 0
    loc = Point(x=0, y=0)
    tests = {idx: {} for idx in range(size.y)}
    while loc is not None:
        if loc.y not in tests:
            tests[loc.y] = {}
        ioo, loc2 = paint(loc, size, tests, pipes)
        if ioo:
            rv += 1
        tests[loc.y][loc.x] = ioo
        loc = loc2

    for y in range(size.y):
        line = ""
        for x in range(size.x):
            if pipes[y][x] and pipes[y][x].valid:
                line += "*"
            elif tests[y][x]:
                line += "I"
            else:
                line += "O"
        log(line)

    return rv


if __name__ == "__main__":
    main()
