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

    def fromLine(self, line):
        self.x, self.y, self.z = map(int, line.split(",", 3))

    def c(self):
        return (self.x, self.y, self.z)


@dataclass
class Brick:
    p1: Point = None
    p2: Point = None

    def __init__(self, id, line):
        self.id = id
        self.supports = {}
        self.sits_on = []
        self.p1 = Point()
        self.p1.fromLine(line.split("~", 2)[0])
        self.p2 = Point()
        self.p2.fromLine(line.split("~", 2)[1])

    def iterCoords(self):
        rv = []
        dx, dy, dz = (
            abs(self.p1.x - self.p2.x),
            abs(self.p1.y - self.p2.y),
            abs(self.p1.z - self.p2.z),
        )
        for z in range(dz + 1):
            for y in range(dy + 1):
                for x in range(dx + 1):
                    rv.append(
                        Point(
                            min(self.p1.x, self.p2.x) + x,
                            min(self.p1.y, self.p2.y) + y,
                            min(self.p1.z, self.p2.z) + z,
                        )
                    )
        return rv

    def addToMap(self, mapx):
        for coord in [c.c() for c in self.iterCoords()]:
            mapx[coord] = self

    def removeFromMap(self, mapx):
        for coord in [c.c() for c in self.iterCoords()]:
            del mapx[coord]

    def getHighestZ(self) -> int:
        if self.p1.z != self.p2.z:
            return max(self.p1.z, self.p2.z)
        return self.p1.z

    def getLowestCoords(self):
        # Vertical piece, return lowest single cube since it's a vertical
        if self.p1.z != self.p2.z:
            return [Point(self.p1.x, self.p1.y, min(self.p1.z, self.p2.z))]

        # Return all coordinates since this is a flat piece and therefore
        # every point is the lowest
        return self.iterCoords()

    def projectDownward(self, mapx, coord: Point):
        # Project a particular coordinate downward (z) through the map and
        # return the brick that it hits
        for tz in range(coord.z - 1, 0, -1):
            brck = mapx.get((coord.x, coord.y, tz), None)
            if brck is not None:
                return brck
        return None

    def supportedBy(self, mapx):
        # Return list of bricks we're touching or an empty list if not
        rv = {}
        for coord in self.getLowestCoords():
            tc = (coord.x, coord.y, coord.z - 1)
            if tc in mapx:
                rv[mapx[tc].id] = mapx[tc]
        return rv.values()

    def connect(self, mapx):
        self.sits_on = self.supportedBy(mapx)
        for sits in self.sits_on:
            sits.supports[self.id] = self

    def sink(self, mapx):
        # Iterate over our lowest coords and sink them, then see which
        # ones we need to keep
        bricks = list(
            filter(
                None, [self.projectDownward(mapx, c) for c in self.getLowestCoords()]
            )
        )

        # if we have no bricks then our miniminum is 0, so default that
        minz = max([brick.getHighestZ() for brick in bricks] if bricks else [0]) + 1
        # log(self, "sinks to", bricks, minz)

        # un-map ourselves, translate down, etc
        self.removeFromMap(mapx)
        if self.p1.z != self.p2.z:
            z1, z2 = minz, minz + abs(self.p1.z - self.p2.z)
            self.p1.z, self.p2.z = z1, z2
        else:
            self.p1.z = minz
            self.p2.z = minz
        self.addToMap(mapx)

    def __repr__(self):
        return "[Brick %d (%d,%d,%d)-(%d,%d,%d) on (%s) under (%s)]" % (
            self.id,
            self.p1.x,
            self.p1.y,
            self.p1.z,
            self.p2.x,
            self.p2.y,
            self.p2.z,
            [b.id for b in self.sits_on],
            [int(b) for b in self.supports.keys()],
        )


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
    rv, mapx = [], defaultdict(int)

    for line in inp:
        rv.append(Brick(len(rv) + 1, line))
        rv[-1].addToMap(mapx)

    return rv, mapx


def part1(inp):
    bricks, mapx = inp

    def pb():
        for z in range(15, -1, -1):
            line = str(z) + " "
            for x in range(0, 10):
                p = False
                for y in range(0, 10):
                    if (x, y, z) in mapx:
                        p = True
                line += "*" if p else "."
            log(line)

    # cause the bricks to fall based on seeing the least far that each
    # coordinate can descend ...

    rv = 0

    unsupported = True
    while unsupported:
        for br in bricks:
            br.sink(mapx)
        unsupported = False
        for br in bricks:
            if br.p1.z == 1 or br.p2.z == 1:
                continue
            if len(br.supportedBy(mapx)) == 0:
                unsupported = True

    for br in bricks:
        br.connect(mapx)

    rv = []
    for br in bricks:
        anyOnly = False
        for br2 in br.supports.values():
            if len(br2.sits_on) == 1:
                anyOnly = True
        if not anyOnly:
            rv.append(1)
        continue

        # the slow way
        br.removeFromMap(mapx)
        unsupported = False
        for br2 in bricks:
            if br == br2:
                continue
            if br2.p1.z == 1 or br2.p2.z == 1:
                continue
            if len(br2.supportedBy(mapx)) == 0:
                unsupported = True
        if not unsupported:
            log(br, "can be removed!")
            rv.append(rv)
        else:
            log(br, "CANNOT")
        br.addToMap(mapx)

    return len(rv)


def part2(inp):
    bricks, mapx = inp

    def pb():
        for z in range(15, -1, -1):
            line = str(z) + " "
            for x in range(0, 10):
                p = False
                for y in range(0, 10):
                    if (x, y, z) in mapx:
                        p = True
                line += "*" if p else "."
            log(line)

    # cause the bricks to fall based on seeing the least far that each
    # coordinate can descend ...

    rv = 0

    unsupported = True
    while unsupported:
        for br in bricks:
            br.sink(mapx)
        unsupported = False
        for br in bricks:
            if br.p1.z == 1 or br.p2.z == 1:
                continue
            if len(br.supportedBy(mapx)) == 0:
                unsupported = True

    for br in bricks:
        br.connect(mapx)

    def count(brick):
        # Given a brick, count how many bricks would fall based on our movement,
        # which means counting all bricks that ONLY connect down to us and have
        # no other support
        ct, lst, bricks = 0, list(brick.supports.values()), set([brick.id])
        while lst:
            brick = lst.pop(0)
            if brick.id in bricks:
                continue

            # get a list of sits
            sits_on = set([b.id for b in brick.sits_on])

            # fully contained in our existing set means it will fall
            if len(sits_on - bricks):
                # log("EXCL", brick, sits_on)
                continue
            # log("INCL", brick, sits_on)
            ct += 1
            bricks.add(brick.id)

            # now add the things it supports
            lst += list(brick.supports.values())

        return ct

    rv = 0
    for br in bricks:
        ct = count(br)
        log(br, ct)
        rv += ct

    return rv


if __name__ == "__main__":
    main()
