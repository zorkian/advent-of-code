from .day import Day
import re


class Day19(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=19, use_test_data=use_test_data)

    def parse_input(self):
        first_line = self.input_data[0]
        self.elements = set(first_line.split(', '))
        self.maxlen = max(map(len, self.elements))
        self.regex_pattern = re.compile('^(' + '|'.join(map(re.escape, self.elements)) + ')+$')

        # Skip the blank line
        self.input_data = self.input_data[2:]
        self.rest_of_lines = self.input_data

    def solve_part_one(self):
        return sum(1 for line in self.rest_of_lines if self.regex_pattern.match(line))

    def count_matches(self, line, depth=0, memo=None):
        if memo is None:
            memo = {}

        if line in memo:
            return memo[line]

        if not line:
            return 1

        if len(line) == 1:
            if line in self.elements:
                return 1
            else:
                return 0

        matches = 0
        for idx in range(1, min(len(line), self.maxlen) + 1):
            if line[:idx] in self.elements:
                matches += self.count_matches(line[idx:], depth + 4, memo)

        memo[line] = matches
        return matches

    def solve_part_two(self):
        ct = 0
        for line in self.rest_of_lines:
            n = self.count_matches(line)
            print(f"Line: {line} -- Matches: {n}")
            ct += n
        return ct
