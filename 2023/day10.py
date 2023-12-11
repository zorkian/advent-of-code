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
    size = Point(x, y)

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


def neighborCoordsFromLoc(loc):
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


def paint(loc, size, pipes, tests):
    coords = [loc]
    paintable = {}
    hitWall = False

    while coords:
        coord = coords.pop(0)

        # if out of range, ignore
        if coord.x < 0 or coord.y < 0 or coord.x >= size.x or coord.y >= size.y:
            continue

        # if this is a pipe, do nothing and return
        if pipes[coord.y].get(coord.x, None):
            continue

        # skip if we've been here
        if coord in paintable:
            continue

        # include this in the space we're seeing
        paintable[coord] = True

        # wall if we're on the edge
        hitWall = hitWall or (
            coord.x == 0
            or coord.y == 0
            or coord.x == size.x - 1
            or coord.y == size.y - 1
        )

        # get neighbor coords to continue testing
        coords += neighborCoordsFromLoc(coord)

    # now, fill in paintables with whether we hit wall
    for coord in paintable:
        tests[coord.y][coord.x] = not hitWall


def part2(inp):
    start, size, pipes = inp

    # start by inflating the map so that we can properly account for spaces
    # "between" pipes
    npipes = {}
    for y in pipes:
        npipes[y * 2] = {}
        npipes[y * 2 + 1] = {}
        for x in pipes[y]:
            pipe = pipes[y][x]
            if pipe is not None:
                pipe.x *= 2
                pipe.y *= 2
                npipes[pipe.y][pipe.x] = pipe

    # embiggen!
    pipes = npipes
    size = Point(size.x * 2 - 1, size.y * 2 - 1)

    # fill in pipes
    for y in range(size.y):
        for x in range(size.x):
            if y not in pipes or x not in pipes[y]:
                continue
            pipe = pipes[y][x]
            if pipe is not None:
                # put in a pipe between us and p1, if not done yet
                if pipe.p1.x % 2 == 0 and pipe.p1.y % 2 == 0:
                    p1 = Point(
                        pipe.x + int((pipe.p1.x - pipe.x) / 2),
                        pipe.y + int((pipe.p1.y - pipe.y) / 2),
                    )
                    pipes[p1.y][p1.x] = Pipe(p1.x, p1.y, pipe, pipe.p1)
                    if pipe.p1.p1 == pipe:
                        pipe.p1.p1 = pipes[p1.y][p1.x]
                    elif pipe.p1.p2 == pipe:
                        pipe.p1.p2 = pipes[p1.y][p1.x]
                    else:
                        raise Exception("fuck3")
                    pipe.p1 = pipes[p1.y][p1.x]

                # now repeat for our p2 pipe
                if pipe.p2.x % 2 == 0 and pipe.p2.y % 2 == 0:
                    p2 = Point(
                        pipe.x + int((pipe.p2.x - pipe.x) / 2),
                        pipe.y + int((pipe.p2.y - pipe.y) / 2),
                    )
                    pipes[p2.y][p2.x] = Pipe(p2.x, p2.y, pipe, pipe.p1)
                    if pipe.p2.p1 == pipe:
                        pipe.p2.p1 = pipes[p2.y][p2.x]
                    elif pipe.p2.p2 == pipe:
                        pipe.p2.p2 = pipes[p2.y][p2.x]
                    else:
                        raise Exception("fuck3")
                    pipe.p2 = pipes[p2.y][p2.x]

    # now start BFSing from each point
    tests = {y: {} for y in range(size.y)}
    for y in range(size.y):
        for x in range(size.x):
            # if this point is already calculated, skip it
            if tests[y].get(x, None) is not None:
                continue

            # fill from this point
            paint(Point(x, y), size, pipes, tests)

    rv = 0

    for y in range(size.y):
        if y % 2 == 1:
            continue
        line = ""
        for x in range(size.x):
            if x % 2 == 1:
                continue
            if x in pipes[y] and pipes[y][x] and pipes[y][x].valid:
                line += "*"
            elif tests[y].get(x, False):
                line += "I"
                rv += 1
            else:
                line += "O"
        log(line)

    return rv


if __name__ == "__main__":
    main()
