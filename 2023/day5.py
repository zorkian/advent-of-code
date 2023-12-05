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
    prefix = "inputs/day" + sys.argv[0].split(".")[0][-1] + "."
    with open(prefix + ("test" if test else "input")) as f:
        return [l.strip() for l in f.readlines()]


def munge_input(inp):
    """
    Convert the input lines into whatever structure we need to handle the
    problem of the day.
    """
    seeds = []
    convs = defaultdict(lambda: defaultdict(int))

    start, end = None, None
    for line in inp:
        if line.startswith("seeds:"):
            seeds = map(int, line.split(":", 2)[1].split())
        elif line.endswith(" map:"):
            start, to, end = line.split(" ", 2)[0].split("-", 3)
        elif line != "":
            dst, src, ct = map(int, line.split())
            convs[start][(src, src + ct - 1)] = dst - src

    for test in convs.keys():
        keys = list(convs[test].keys())
        keys.sort()

        last_end = None
        for src_start, src_end in keys:
            if last_end is None and src_start > 0:
                convs[test][(0, src_start - 1)] = 0
            if last_end is not None and last_end < (src_start - 1):
                convs[test][(last_end + 1, src_start - 1)] = 0
            last_end = src_end

        convs[test][(last_end + 1, last_end + 1000000000000000000)] = 0

    return [seeds, convs]


def part1(inp):
    seeds, convs = inp
    order = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity"]

    rv = None
    for seed in seeds:
        idx = seed
        for test in order:
            hit = False
            for src_start, src_end in convs[test].keys():
                log("Test", idx, "vs", src_start, src_end)
                if not hit and idx >= src_start and idx <= src_end:
                    log("Hit and adding", convs[test][(src_start, src_end)])
                    idx += convs[test][(src_start, src_end)]
                    hit = True
            log("Finished", test, "at", idx)
        if rv is None or idx < rv:
            rv = idx

    return rv


def part2(inp):
    seeds, convs = inp
    order = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity"]

    seeds = list(seeds)
    sds = []
    for idx in range(int(len(seeds) / 2)):
        sds.append((seeds[idx * 2], seeds[idx * 2] + seeds[idx * 2 + 1] - 1))
    seeds = sds

    def min_and_len(start, length, remaining):
        log("min_and_len(", start, ",", length, ",", remaining, ")")
        # Given a starting seed number, run through the next in the order and convert,
        # returning the length of the last list + the start number (which will be the
        # minimum location)
        test = remaining.pop()
        test_keys = list(convs[test].keys())
        test_keys.sort()

        log("source ranges:", [(key, convs[test][key]) for key in test_keys])

        for src_start, src_end in test_keys:
            if start >= src_start and start <= src_end:
                length = min(length, src_end - start + 1)
                if remaining:
                    # We have more to test, recurse but use the converted destination
                    # value
                    return min_and_len(
                        start + convs[test][(src_start, src_end)], length, remaining
                    )
                else:
                    # If nothing remaining, return the ID we have and how big the
                    # final range is to src_end
                    log("Returning1:", (start, length))
                    return (start, length)
        raise Exception("no pseudo-range found")

    # Iterate each seed pair and start slicing the chunks up based on the minimally
    # cascading interval (I doubt this sentence makes sense to a reader, but it does
    # in my head... sorry :))
    min_so_far = None
    for start, end in seeds:
        while start <= end:
            log()
            log("STARTING AT:", start, end)
            # Prepare list of order (in reverse, since we pop)
            remaining = order.copy()
            remaining.reverse()

            # Get min and len to slice
            mn, ln = min_and_len(start, end - start + 1, remaining)
            start += ln

            # See the minimum of this section
            if min_so_far is None:
                min_so_far = mn
            else:
                min_so_far = min(mn, min_so_far)

    return min_so_far


if __name__ == "__main__":
    main()
