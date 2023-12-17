import os
import logging

import aocd

from dataclasses import dataclass
from typing import Dict


@dataclass
class Point:
    x: int = 0
    y: int = 0
    z: int = 0


@dataclass
class Grid:
    width: int = 0
    height: int = 0
    # points: Dict[Point, str] = {}


class AocPart:
    TEST_INPUT = None
    TEST_RESULT = None

    def test(self):
        assert self.result(data=self.TEST_INPUT) == self.TEST_RESULT, (
            "test for " + str(type(self)) + " did not pass"
        )

    def run(self, data):
        raise Exception("run() not implemented")

    def result(self, day=None, year=None, data=None):
        if data is None:
            data = aocd.get_data(day=day, year=year)
        return self.run(data)


def read_grids(inp):
    # Read a series of grids separated by one or more blank lines. The
    # grids are assumed to be character grids.
    rv = []

    y, grid = 0, None
    for line in inp:
        if not line:
            if grid is not None:
                rv.append(grid)
                grid = None
                continue
        if grid is None:
            grid = Grid()
            y = 0
        x = 0
        for char in line:
            grid.points[Point(x, y)] = char
            x += 1
        y += 1

    return rv


def log(*args, **kwargs):
    logging.warning(*args, **kwargs)
