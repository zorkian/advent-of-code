import click
import sys

from collections import defaultdict
from hashlib import md5

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
    # #OO..#....
    rv = []
    for line in inp:
        rv.append([])
        rv[-1] += [c for c in line]
    return rv


def tiltNorth(inp):
    for x in range(len(inp[0])):
        open = []
        for y in range(len(inp)):
            if inp[y][x] == "#":
                open = []
            elif inp[y][x] == ".":
                open.append(y)
            elif inp[y][x] == "O":
                if not open:
                    continue
                inp[open.pop(0)][x] = "O"
                inp[y][x] = "."
                open.append(y)
    return inp


def tiltSouth(inp):
    for x in range(len(inp[0])):
        open = []
        for y in reversed(range(len(inp))):
            if inp[y][x] == "#":
                open = []
            elif inp[y][x] == ".":
                open.append(y)
            elif inp[y][x] == "O":
                if not open:
                    continue
                inp[open.pop(0)][x] = "O"
                inp[y][x] = "."
                open.append(y)
    return inp


def tiltEast(inp):
    for y in range(len(inp)):
        open = []
        for x in reversed(range(len(inp[y]))):
            if inp[y][x] == "#":
                open = []
            elif inp[y][x] == ".":
                open.append(x)
            elif inp[y][x] == "O":
                if not open:
                    continue
                inp[y][open.pop(0)] = "O"
                inp[y][x] = "."
                open.append(x)
    return inp


def tiltWest(inp):
    for y in range(len(inp)):
        open = []
        for x in range(len(inp[y])):
            if inp[y][x] == "#":
                open = []
            elif inp[y][x] == ".":
                open.append(x)
            elif inp[y][x] == "O":
                if not open:
                    continue
                inp[y][open.pop(0)] = "O"
                inp[y][x] = "."
                open.append(x)
    return inp


def pr(inp):
    for y in range(len(inp)):
        line = ""
        for x in range(len(inp[y])):
            line += inp[y][x]
        log(line)


def part1(inp):
    rv = 0

    pattern = tiltNorth(inp)
    for y in range(len(pattern)):
        ct = 0
        for x in range(len(pattern[y])):
            if pattern[y][x] == "O":
                ct += 1
        rv += ct * (len(pattern) - y)

    return rv


def part2(inp):
    SIZE = 1000000000

    tmp = []
    lookup = {}
    for idx in range(SIZE):
        if idx % 100000 == 0:
            log(tmp)
        inp = tiltEast(tiltSouth(tiltWest(tiltNorth(inp))))

        hash = md5("".join(["".join(c) for c in inp]).encode("utf-8")).hexdigest()
        if hash not in tmp:
            tmp.append(hash)
            lookup[hash] = [c.copy() for c in inp]
            continue

        # cycle detected, now we know the head and length
        head = tmp.index(hash)
        length = len(tmp) - head
        pos = head + ((SIZE - head) % length) - 1

        log(
            "cycle detected at",
            idx,
            "head at",
            head,
            "length",
            length,
            "calculated",
            pos,
        )

        # get weight now
        rv = 0
        for y in range(len(lookup[tmp[pos]])):
            ct = 0
            for x in range(len(lookup[tmp[pos]][y])):
                if lookup[tmp[pos]][y][x] == "O":
                    ct += 1
            rv += ct * (len(lookup[tmp[pos]]) - y)
        return rv


if __name__ == "__main__":
    main()
