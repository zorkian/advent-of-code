import click
import re
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

    out = []
    for line in inp:
        f, l = line.split(" ", 2)
        # f = list(filter(lambda x: x, re.sub("\.+", ".", f).split(".")))
        out.append([f, list(map(int, l.split(",")))])
    return out


def score(line):
    rv = []
    for strset in filter(lambda x: x, line.split(".")):
        rv.append(len(strset))
    return rv


def permutations(line, sets):
    # Given input line like "???.###" try to place the first unplaced ?
    # and see if it matches once there are no more question marks
    try:
        idx = line.index("?")
    except ValueError:
        # BASE CASE.
        # no more question marks, score this and see if it works
        log(line, score(line))
        if score(line) == sets:
            return 1
        else:
            return 0

    # idx is now first question mark, try replacing it with all of the
    # possibilities and sum the things that worked
    return permutations(line[:idx] + "." + line[idx + 1 :], sets) + permutations(
        line[:idx] + "#" + line[idx + 1 :], sets
    )


MEMOS = {}


def permutations2(line, sets, sofar=""):
    log("PERM2", line, sets, sofar + line)
    memokey = line + ":" + ",".join(map(str, sets))
    if memokey in MEMOS:
        return MEMOS[memokey]

    def memoize(val):
        log("MEMO:", memokey, val)
        MEMOS[memokey] = val
        return val

    # Base case: no more sets, the line must consist of periods or question
    # marks from this point forward
    if len(sets) == 0:
        if "#" in line:
            return memoize(0)
        log("SCORED (base case)", sofar + line)
        return memoize(1)

    # If we're down to the last hash and set of 1
    if line == "#" and len(sets) == 1 and sets[0] == 1:
        log("SCORED (last hope)", sofar + line)
        return memoize(1)

    # Second fast exit: if there's no possible way to satisfy, then we don't
    # need to continue
    if len(line) < sum(sets) + len(sets) - 1:
        return memoize(0)

    # Iterate the line and try to match the first set we see, and construct
    # it out of ?s if we can't, note you need . as separators
    ct = 0
    for idx in range(len(line)):
        if line[idx] == ".":
            # Period with zero in the counter means skip/ignore, this is a
            # leading or doubled, we don't care
            if ct == 0:
                sofar += "."
                continue

            # If we hit a period, and count is non-zero, we've hit a forced
            # end of the run and this means we're done ... if it matches our
            # target, we continue down the rabbit hole, if it's not, then we
            # abort because we cannot succeed down this path
            if ct != sets[0]:
                # log("BUST ct != sets[0]")
                return memoize(0)

            # Count matches, continue with the next permutation
            # log("PERMUTING OFF .")
            return permutations2(line[idx + 1 :], sets[1:], sofar + ("#" * ct) + ".")

        elif line[idx] == "#":
            # This is a forced increment, we can't mess with this
            ct += 1

            # If we've busted (gone over what we're looking for) then this can't
            # possibly be a win state, return
            if ct > sets[0]:
                # log("BUST ct > sets[0]")
                return memoize(0)

        elif line[idx] == "?":
            # This means we could treat this as either a dot or a question mark,
            # try to recurse with either option, but which we pick has to be smart
            # based on where we are
            if ct > 0 and ct == sets[0]:
                # Has to be a period, since this is a good set at this spot, we
                # can't just make it a hash (would increase ct)
                return memoize(
                    permutations2("." + line[idx + 1 :], sets[1:], sofar + ("#" * ct))
                )

            elif ct > 0 and ct < sets[0]:
                # We aren't at value yet, this MUST be a hash, and we can just
                # continue our loop here -- no need to recurse
                ct += 1

            elif ct > 0 and ct > sets[0]:
                # shouldn't happen
                raise Exception("fuck2")

            else:
                # We have nothing, this could either be a period or hash, and we
                # should not consume a set... so continue on with both
                return memoize(
                    permutations2("." + line[idx + 1 :], sets, sofar + ("#" * ct))
                    + permutations2("#" + line[idx + 1 :], sets, sofar + ("#" * ct))
                )

        else:
            raise Exception("fuck")

    # If we get here, do a final check to see if we matched, because
    # we just consumed everything
    if ct == sets[0] and len(sets) == 1:
        return memoize(1)
    return memoize(0)


def part1(inp):
    rv = 0
    for test in inp:
        rv += permutations(*test)
    return rv


def part2(inp):
    rv = 0
    for idx in range(len(inp)):
        test = inp[idx]
        i = permutations2("?".join([test[0]] * 5), test[1] * 5)
        print(idx, test, i)
        rv += i
    return rv


if __name__ == "__main__":
    main()
