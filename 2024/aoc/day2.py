from .day import Day


class Day2(Day):
    def __init__(self, use_test_data=False):
        self.parsed_data = []
        super().__init__(day_number=2, use_test_data=use_test_data)

    def parse_input(self):
        for line in self.input_data:
            parsed_line = list(map(int, line.split()))
            self.parsed_data.append(parsed_line)

    def solve_part_one(self):
        safe_count = 0
        for seq in self.parsed_data:
            if len(seq) < 2:
                continue
            is_increasing = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
            is_decreasing = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
            if (is_increasing or is_decreasing) and all(1 <= abs(seq[i] - seq[i + 1]) <= 3 for i in range(len(seq) - 1)):
                safe_count += 1
        return safe_count

    def solve_part_two(self):
        safe_count = 0
        for seq in self.parsed_data:
            if len(seq) < 2:
                continue

            def check_sequence(seq):
                return (all(seq[i] < seq[i + 1] for i in range(len(seq) - 1)) or
                        all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))) and \
                        all(1 <= abs(seq[i] - seq[i + 1]) <= 3 for i in range(len(seq) - 1))

            if check_sequence(seq):
                safe_count += 1
            else:
                for ignore_index in range(len(seq)):
                    if check_sequence([seq[i] for i in range(len(seq)) if i != ignore_index]):
                        safe_count += 1
                        break  # Only count this sequence once
        return safe_count
