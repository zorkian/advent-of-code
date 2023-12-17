#
# solving!
#

import importlib


def solver(year, day, data):
    mod_name = "aoc.aoc{}.day{}".format(year, day)
    mod = importlib.import_module(mod_name)
    a = mod.part1(data)
    b = mod.part2(data)
    return a, b
