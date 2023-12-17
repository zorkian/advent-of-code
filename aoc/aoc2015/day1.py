import collections
import logging

from aoc.utils import AocPart, log


class Part1(AocPart):
    TEST_INPUT = """
))(((((
"""
    TEST_RESULT = 3

    def run(self, data):
        data = [l.strip() for l in data]

        ct = collections.defaultdict(int)
        for char in data:
            ct[char] += 1
        return ct["("] - ct[")"]


class Part2(AocPart):
    TEST_INPUT = """
"""
    TEST_RESULT = 0

    def run(self, data):
        data = [l.strip() for l in data]
        log(data)

        depth, pos = 0, 1
        for char in data:
            if char == ")":
                if depth == 0:
                    return pos
                depth -= 1
            elif char == "(":
                depth += 1
            pos += 1
        return 0


if __name__ == "__main__":
    Part1().test()
    Part2().test()
    print(Part1().result(), Part2().result())
