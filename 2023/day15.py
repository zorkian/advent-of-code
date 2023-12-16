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
    return [inp[0].split(",")]


def hash(inp):
    cv = 0
    for char in inp:
        cv = ((cv + ord(char)) * 17) % 256
    return cv


def part1(inp):
    rv = 0

    for line in inp[0]:
        rv += hash(line)

    return rv


def part2(inp):
    boxes = [[] for idx in range(256)]
    for line in inp[0]:
        flen, rmv = 0, False
        if line.endswith("-"):
            label, rmv = line[:-1], True
        else:
            label, flen = line.split("=")
        box = hash(label)
        if rmv:
            log("remove", label, "from", box)
            boxes[box] = list(
                filter(lambda bx: False if bx[0] == label else True, boxes[box])
            )
            log("=", boxes[box])
        else:
            log("add", label, "to", box)
            if label in map(lambda bx: bx[0], boxes[box]):
                boxes[box] = list(
                    map(
                        lambda bx: bx if bx[0] != label else (label, int(flen)),
                        boxes[box],
                    )
                )
            else:
                boxes[box].append((label, int(flen)))
            log("=", boxes[box])

    log("")

    rv = 0

    for idx in range(len(boxes)):
        if len(boxes[idx]):
            log(idx, boxes[idx])
            for pidx in range(len(boxes[idx])):
                rv += (idx + 1) * (pidx + 1) * boxes[idx][pidx][1]

    return rv


if __name__ == "__main__":
    main()
