from .day import Day
from functools import lru_cache


class Day11(Day):
    def __init__(self, use_test_data=False, debug=False):
        self.debug = debug
        super().__init__(day_number=11, use_test_data=use_test_data)

    def parse_input(self):
        if self.input_data:
            if self.debug:
                print(f"Input data: {self.input_data}")
            self.parsed_data = list(map(int, self.input_data[0].split()))
            if self.debug:
                print(f"Parsed data: {self.parsed_data}")
        else:
            self.parsed_data = []

    @lru_cache(None)
    def process_number_p2(self, number, count):
        if count <= 0:
            return 1
        if number == 0:
            return self.process_number_p2(1, count - 1)
        num_str = str(number)
        if len(num_str) % 2 == 0:
            mid = len(num_str) // 2
            return self.process_number_p2(int(num_str[:mid]), count - 1) + self.process_number_p2(int(num_str[mid:]), count - 1)
        return self.process_number_p2(number * 2024, count - 1)

    def process_number(self, number):
        if number == 0:
            return [1]
        num_str = str(number)
        if len(num_str) % 2 == 0:
            mid = len(num_str) // 2
            return [int(num_str[:mid]), int(num_str[mid:])]
        return [number * 2024]

    @lru_cache(None)
    def process_list(self, numbers, count):
        if count <= 0:
            return numbers
        total_numbers = []
        for number in numbers:
            total_numbers.extend(self.process_number(number))
        return self.process_list(tuple(total_numbers), count - 1)

    def solve_part_one(self):
        return sum([self.process_number_p2(i, 25) for i in self.parsed_data])

    def solve_part_two(self):
        return sum([self.process_number_p2(i, 75) for i in self.parsed_data])
