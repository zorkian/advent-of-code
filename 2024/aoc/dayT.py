from .day import Day


class DayT(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=T, use_test_data=use_test_data)

    def parse_input(self):
        for line in self.input_data:
            pass

    def solve_part_one(self):
        return 0

    def solve_part_two(self):
        return 0
