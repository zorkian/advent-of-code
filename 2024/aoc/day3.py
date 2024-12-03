from .day import Day


class Day3(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=3, use_test_data=use_test_data)

    def parse_input(self):
        for line in self.input_data:
            pass

    def solve_part_one(self):
        import re
        total = 0
        pattern = r'mul\((\d+),(\d+)\)'

        for line in self.input_data:
            matches = re.findall(pattern, line)
            for x, y in matches:
                total += int(x) * int(y)

        return total

    def solve_part_two(self):
        import re
        total = 0
        pattern = r'mul\((\d+),(\d+)\)'

        segments = ''.join(self.input_data).split("do()")
        for segment in segments:
            segment = segment.split("don't()")[0]
            matches = re.findall(pattern, segment)
            for x, y in matches:
                total += int(x) * int(y)

        return total
