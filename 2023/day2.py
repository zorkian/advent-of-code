import click
import collections
import sys


@click.command()
@click.option("-p1", is_flag=True, help="Run part 1.")
@click.option("-p2", is_flag=True, help="Run part 2.")
@click.option("-test", is_flag=True, help="Use test inputs.")
def main(p1, p2, test):
    inp = munge_input(load_input(test))
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
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    games = collections.defaultdict(lambda: collections.defaultdict(int))
    for line in inp:
        l, r = line.split(":")
        gameid = int(l.split(" ")[1])
        for game in r.split(";"):
            for color in game.split(","):
                ct, col = color.strip().split(" ", 2)
                games[gameid][col] = max(int(ct), games[gameid][col])
    return games


def part1(inp):
    # only 12 red cubes, 13 green cubes, and 14 blue cubes
    maxes = {"red": 12, "green": 13, "blue": 14}

    rv = 0
    for gameid, game in inp.items():
        keep = True
        for col, mx in maxes.items():
            if game[col] > mx:
                keep = False
        if keep:
            rv += gameid
    return rv


def part2(inp):
    rv = 0
    for gameid, game in inp.items():
        tmp = 1
        for mx in game.values():
            tmp *= mx
        rv += tmp
    return rv


if __name__ == "__main__":
    main()
