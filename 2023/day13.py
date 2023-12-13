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


def toNumber(line):
    return int(line.replace("#", "1").replace(".", "0"), 2)


def findSplitx(nums):
    lst = []
    for idx in range(len(nums)):
        # if we're matching, our most recent number, walk back and see
        # if it matches
        # log(lst, nums[idx])
        if len(lst) == 0:
            lst.append(nums[idx])
            continue

        # see if here forward matches there backwards
        if lst[-1] == nums[idx]:
            matches = True
            rlst = list(reversed(lst))
            for i in range(len(rlst)):
                if idx + i < len(nums):
                    if rlst[i] != nums[idx + i]:
                        matches = False
            if matches:
                return idx

        lst.append(nums[idx])


PO2 = set([2**idx for idx in range(0, 32)])


def findSplit(inp, with_bit_flip=False):
    # given a list of numbers, figure out if a single bit change can turn
    # them into a matching set by looking at xors and seeing if it results
    # in a single bit being different (non-zero)

    # a b c d e f
    #  |
    #

    mx = len(inp)
    log("rb1", inp)

    rvs = []
    for sidx in range(1, mx):
        # assume we split at this location, into two halves left and right,
        # and then start seeing if the xor lines up if we're flipping bits
        flipped, valid = False, True
        left = list(reversed(inp[:sidx]))
        right = inp[sidx:]

        # if we're in bitflip mode, we have to force flip a bit somewhere,
        # but it's only worth doing if the two sections are "one bit off"
        for midx in range(min(len(left), len(right))):
            if not valid or left[midx] == right[midx]:
                log(midx, left, right)
                continue

            # if we're not flipping bits, we immediately are invalid trying
            # to split at this location
            if not with_bit_flip:
                valid = False
                continue

            if (left[midx] ^ right[midx]) in PO2:
                # the XOR is a power of two, which means there's exactly 1
                # bit that is set in one but not the other
                if flipped:
                    # we already flipped a bit, we can't flip again, this means
                    # that we don't have a true match here at this location
                    # so we should continue on to the next potential split
                    valid = False
                else:
                    # pretend we flip a bit
                    log("FLIPPED", sidx)
                    flipped = True
            else:
                # More than one bit of difference so just abort and continue
                valid = False

        # If we flipped a bit and this is valid, we know that we can do a
        # reflection around this point
        if valid and (with_bit_flip == False or flipped):
            rvs.append(sidx)

    # now try
    log(">>>", inp, rvs)
    if len(rvs) > 1:
        raise Exception("fuck")

    return rvs[0] if len(rvs) else 0


def munge_input(inp):
    """
    Convert the input lines into whatever structure we need to handle the
    problem of the day.
    """
    rv = []
    pattern, verts, horizs = [], [], []
    for line in inp:
        if line:
            pattern.append(line)
        else:
            # parse the pattern into verts and horizs
            for line in pattern:
                horizs.append(toNumber(line))

            # verticals
            verts = ["" for idx in range(len(pattern[0]))]
            for idx in range(len(pattern)):
                for lidx in range(len(pattern[0])):
                    verts[lidx] += pattern[idx][lidx]
            verts = [toNumber(num) for num in verts]

            # append to rv
            rv.append((pattern, horizs, verts))
            pattern, horizs, verts = [], [], []

    return rv


def part1(inp):
    rv = 0

    for parts in inp:
        pattern, horizs, verts = parts

        # see if horizontal split
        idx = findSplit(horizs)
        if idx and idx > 0:
            log("horizs", idx)
            rv += idx * 100

        idx = findSplit(verts)
        if idx and idx > 0:
            log("verts", idx)
            rv += idx

    return rv


def part2(inp):
    rv = 0

    for parts in inp:
        pattern, horizs, verts = parts

        # see if horizontal split
        log("TRY", pattern)
        hv = findSplit(horizs, with_bit_flip=True) * 100
        # hvn = findSplit(horizs) * 100
        # if hv != 0 and hv == hvn:
        #   log(hv, hvn)
        #    raise Exception(pattern)
        vv = findSplit(verts, with_bit_flip=True)
        # vvn = findSplit(verts)
        # if vv != 0 and vv == vvn:
        #    log(vv, vvn)
        #    raise Exception(pattern)
        if hv == 0 and vv == 0:
            log("NO", horizs, verts)
            raise Exception(pattern)
        elif hv > 0 and vv > 0:
            log("NO", horizs, verts)
            raise Exception(pattern)
        rv += hv + vv

    return rv


if __name__ == "__main__":
    main()
