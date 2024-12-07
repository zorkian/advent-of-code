from .day import Day


class Day7(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=7, use_test_data=use_test_data)

    def parse_input(self):
        self.parsed_data = {}
        for line in self.input_data:
            key, values = line.split(':')
            self.parsed_data[int(key.strip())] = list(map(int, values.strip().split()))

    def solve_part_one(self):
        valid_entries_sum = 0  # To accumulate the sum of valid entries
        counted_entries = set()  # To keep track of counted valid entries
        for result, inputs in self.parsed_data.items():
            for i in range(1 << (len(inputs) - 1)):  # generate all combinations of + and *
                total = inputs[0]
                for j in range(len(inputs) - 1):
                    operator = '+' if (i & (1 << j)) else '*'
                    if operator == '+':
                        total += inputs[j + 1]
                    else:
                        total *= inputs[j + 1]

                if total == result and result not in counted_entries:
                    valid_entries_sum += result
                    counted_entries.add(result)

        return valid_entries_sum

    def solve_part_two(self):
        valid_entries_sum = 0  # To accumulate the sum of valid entries
        counted_entries = set()  # To keep track of counted valid entries

        def recursive_solve(index, total, equation):
            nonlocal valid_entries_sum
            if index == len(inputs) - 1:  # If we have processed all inputs
                if total == result and result not in counted_entries:
                    valid_entries_sum += result
                    counted_entries.add(result)
                    #print(f"Valid: {equation} = {total}")
                else:
                    pass
                    #print(f"Invalid: {equation} = {total}")
                return

            next_input = inputs[index + 1]
            for operator in ('+', '*', '&'):
                new_total = total
                new_equation = equation

                if operator == '+':
                    new_total += next_input
                    new_equation += f" + {next_input}"
                elif operator == '*':
                    new_total *= next_input
                    new_equation += f" * {next_input}"
                elif operator == '&':
                    new_total = int(f"{new_total}{next_input}")
                    new_equation += f" & {next_input}"

                recursive_solve(index + 1, new_total, new_equation)

        for result, inputs in self.parsed_data.items():
            initial_equation = str(inputs[0])  # Initialize the equation string
            recursive_solve(0, inputs[0], initial_equation)

        return valid_entries_sum
