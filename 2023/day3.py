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
    syms = collections.defaultdict(lambda: collections.defaultdict(str))
    nums = collections.defaultdict(lambda: collections.defaultdict(int))
    used = collections.defaultdict(bool)
    number = collections.defaultdict(int)

    def enditx(x, y, num, ctr):
        # End the number and store the adjacencies
        used[ctr] = False
        for ix in range(max(x - len(num), 0), x):
            nums[y][ix] = ctr
        number[ctr] = int(num)

    y, ctr = 0, 0
    for line in inp:
        x = 0
        num = ""
        for chr in line:
            endit = True
            if chr >= "0" and chr <= "9":
                num += chr
                endit = False
            elif chr == ".":
                pass
            else:
                syms[y][x] = chr
            if endit:
                if num != "":
                    ctr += 1
                    enditx(x, y, num, ctr)
                    num = ""
            x += 1
        if num != "":
            ctr += 1
            enditx(x, y, num, ctr)
        y += 1

    return [syms, nums, used, number]


def part1(inp):
    syms, nums, used, number = inp

    # Iterate each symbol and zap any number around it
    for y in syms.keys():
        for x in syms[y].keys():
            for iy in range(max(y - 1, 0), y + 2):
                for ix in range(max(x - 1, 0), x + 2):
                    num = nums[iy][ix]
                    if num > 0:
                        used[num] = True

    rv = 0
    for idx in used.keys():
        if used[idx]:
            rv += number[idx]
    return rv


def part2(inp):
    syms, nums, used, number = inp

    # Iterate each symbol and zap any number around it
    rv = 0
    for y in syms.keys():
        for x in syms[y].keys():
            if syms[y][x] != "*":
                continue
            numbers = set()
            for iy in range(max(y - 1, 0), y + 2):
                for ix in range(max(x - 1, 0), x + 2):
                    num = nums[iy][ix]
                    if num > 0:
                        numbers.add(num)
            numbers = [number[num] for num in numbers]
            if len(numbers) == 2:
                rv += numbers[0] * numbers[1]
    return rv


if __name__ == "__main__":
    main()
