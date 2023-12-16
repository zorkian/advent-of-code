import click
import sys

from collections import defaultdict

VERBOSE = False

EMPTY = 0
VERTICAL = 1
HORIZONTAL = 2
FWDSLASH = 4
BACKSLASH = 8
G_NORTH = 16
G_WEST = 32
G_SOUTH = 64
G_EAST = 128


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

    board = defaultdict(lambda: int)

    y = 0
    for line in inp:
        x = 0
        for char in line:
            board[(x, y)] = [
                {
                    ".": EMPTY,
                    "|": VERTICAL,
                    "-": HORIZONTAL,
                    "\\": BACKSLASH,
                    "/": FWDSLASH,
                }[char],
                0,
            ]
            x += 1
        y += 1

    return (x, y), board


def velToDirection(vel):
    if vel == (1, 0):
        return G_EAST
    elif vel == (-1, 0):
        return G_WEST
    elif vel == (0, 1):
        return G_SOUTH
    elif vel == (0, -1):
        return G_NORTH
    raise Exception("fuck")


def beam(size, board, loc, vel):
    tries = [(loc, vel)]

    while len(tries) > 0:
        loc, vel = tries.pop(0)

        # base case, beam has escaped the board, no more need to track
        if loc[0] < 0 or loc[0] >= size[0] or loc[1] < 0 or loc[1] >= size[1]:
            continue

        # log(size, loc, vel)
        direction = velToDirection(vel)
        x, y = loc

        # if we're landing in a cell that has already energized in the
        # direction we're going, we don't need to re-path this and we
        # can early abort this trace
        if board[loc][1] & direction > 0:
            continue

        # first, energize the square we're in, since we know that this
        # square is off somewhere
        # TODO: probably need to validate that this is true in all cases,
        # I bet there's a bug here
        board[loc][1] |= direction

        # see if this is something fancy
        if board[loc][0] == VERTICAL:
            if direction in (G_WEST, G_EAST):
                # beam split north, south
                tries.append(((x, y - 1), (0, -1)))
                tries.append(((x, y + 1), (0, 1)))
                continue
        elif board[loc][0] == HORIZONTAL:
            if direction in (G_NORTH, G_SOUTH):
                # beam split west, east
                tries.append(((x - 1, y), (-1, 0)))
                tries.append(((x + 1, y), (1, 0)))
                continue
        elif board[loc][0] == FWDSLASH:  # /
            if direction == G_EAST:
                tries.append(((x, y - 1), (0, -1)))
            elif direction == G_WEST:
                tries.append(((x, y + 1), (0, 1)))
            elif direction == G_NORTH:
                tries.append(((x + 1, y), (1, 0)))
            elif direction == G_SOUTH:
                tries.append(((x - 1, y), (-1, 0)))
            continue
        elif board[loc][0] == BACKSLASH:  # \
            if direction == G_EAST:
                tries.append(((x, y + 1), (0, 1)))
            elif direction == G_WEST:
                tries.append(((x, y - 1), (0, -1)))
            elif direction == G_NORTH:
                tries.append(((x - 1, y), (-1, 0)))
            elif direction == G_SOUTH:
                tries.append(((x + 1, y), (1, 0)))
            continue

        # if we get here, nothing fancy happened, continue moving the beam
        # and energize this square
        tries.append(((x + vel[0], y + vel[1]), vel))


def part1(inp):
    # cast a beam from the top left, going right
    size, board = inp
    beam(size, board, (0, 0), (1, 0))

    rv = 0
    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            rv += 1 if board[(x, y)][1] else 0
            line += "#" if board[(x, y)][1] else "."
        log(line)
    return rv


def score(size, board):
    rv = 0
    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            rv += 1 if board[(x, y)][1] else 0
            line += "#" if board[(x, y)][1] else "."
        log(line)
    return rv


def part2(inp):
    size, board = inp

    rv = 0
    for i in range(size[0]):
        # from north, fire south
        b2 = {k: board[k].copy() for k in board.keys()}
        beam(size, b2, (i, 0), (0, 1))
        rv = max(rv, score(size, b2))

        # from south, fire north
        b2 = {k: board[k].copy() for k in board.keys()}
        beam(size, b2, (i, size[1] - 1), (0, -1))
        rv = max(rv, score(size, b2))

        # from west, fire east
        b2 = {k: board[k].copy() for k in board.keys()}
        beam(size, b2, (0, i), (1, 0))
        rv = max(rv, score(size, b2))

        # from east, fire west
        b2 = {k: board[k].copy() for k in board.keys()}
        beam(size, b2, (size[0] - 1, i), (-1, 0))
        rv = max(rv, score(size, b2))

    return rv


if __name__ == "__main__":
    main()
