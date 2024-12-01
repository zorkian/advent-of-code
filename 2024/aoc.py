import click

import aoc


@click.command()
@click.option("--day", default=1, help="Day of the Advent of Code challenge")
@click.option("--test", is_flag=True, help="Use test data")
@click.option(
    "--part",
    type=click.IntRange(0, 2),
    default=0,
    help="Part of the day to run (0 for both, 1 for part one, 2 for part two)",
)
def main(day, test, part):
    day = aoc.get_day(day, test)
    if part == 0:
        day.part_one()
        day.part_two()
    elif part == 1:
        day.part_one()
    elif part == 2:
        day.part_two()


if __name__ == "__main__":
    main()
