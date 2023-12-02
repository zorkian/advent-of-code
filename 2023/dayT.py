import click
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
    return inp


def part1(inp):
    print(inp)
    return 0


def part2(inp):
    print(inp)
    return 0


if __name__ == "__main__":
    main()
