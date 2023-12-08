import click
import math
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
    path = [c for c in inp.pop(0)]
    inp.pop(0)

    ret = {}

    for elems in inp:
        source, rest = elems.split(" = ", 1)
        left, right = rest.split(", ")
        left = left[1:]
        right = right[0:-1]
        ret[source] = (left, right)

    ret["path"] = path
    return ret


def part1(inp):
    rv = 0

    path = inp["path"]
    cur = "AAA"
    while cur != "ZZZ":
        rv += 1
        nxt = path.pop(0)
        path.append(nxt)
        log(cur, nxt)
        cur = inp[cur][0 if nxt == "L" else 1]

    return rv


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def part2(inp):
    rv = 0

    path = inp["path"]

    curs = []
    for tst in inp.keys():
        if tst.endswith("A"):
            curs.append(tst)

    lens = [None for idx in range(len(curs))]

    while True:
        if all(lens):
            break

        rv += 1
        nxt = path.pop(0)
        path.append(nxt)

        for idx in range(len(curs)):
            if lens[idx] is not None:
                continue
            curs[idx] = inp[curs[idx]][0 if nxt == "L" else 1]
            log(idx, curs[idx])
            if curs[idx].endswith("Z"):
                log(idx, "identified at", rv)
                lens[idx] = rv

    lcstart = lcm(lens[0], lens[1])
    for idx in range(len(lens) - 2):
        lcstart = lcm(lcstart, lens[idx + 2])

    return lcstart


if __name__ == "__main__":
    main()
