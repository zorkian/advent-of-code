import click
import collections
import sys

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
    return inp


def part1(inp):
    ct = collections.defaultdict(int)
    for char in inp[0]:
        ct[char] += 1
    return ct['('] - ct[')']


def part2(inp):
    depth, pos = 0, 1
    for char in inp[0]:
        if char == ')':
            if depth == 0:
                return pos
            depth -= 1
        elif char == '(':
            depth += 1
        pos += 1
    return 0


if __name__ == "__main__":
    main()
