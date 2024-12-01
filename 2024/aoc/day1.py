from .day import Day


class Day1(Day):
    def __init__(self, use_test_data=False):
        self.list1 = []
        self.list2 = []
        super().__init__(day_number=1, use_test_data=use_test_data)

    def parse_input(self):
        for line in self.input_data:
            numbers = list(map(int, line.split()))
            self.list1.append(numbers[0])
            self.list2.append(numbers[1])

    def solve_part_one(self):
        self.list1.sort()
        self.list2.sort()
        total_difference = sum(abs(a - b) for a, b in zip(self.list1, self.list2))
        return total_difference

    def solve_part_two(self):
        total_multiplication = 0
        for number in self.list1:
            count = self.list2.count(number)
            total_multiplication += number * count
        return total_multiplication
