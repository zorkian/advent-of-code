from .day import Day


class Day13(Day):
    def __init__(self, use_test_data=False):
        self.button_tokens = {'Button A': 3, 'Button B': 1}
        super().__init__(day_number=13, use_test_data=use_test_data)

    def parse_input(self):
        self.parsed_data = []
        current_block = []

        for line in self.input_data:
            if line.strip():  # If the line is not empty
                current_block.append(line.strip())
            else:  # An empty line indicates the end of a block
                if current_block:
                    self.parsed_data.append(self.parse_block(current_block))
                    current_block = []

        # Add the last block if it exists
        if current_block:
            self.parsed_data.append(self.parse_block(current_block))

    def parse_block(self, block):
        buttons = {}
        prize = {}

        for line in block:
            if line.startswith("Button"):
                name, coordinates = line.split(": ")
                x, y = map(lambda coord: coord[2:], coordinates.split(", "))  # Skip 'X+' or 'Y+'
                buttons[name] = (int(x), int(y))
            elif line.startswith("Prize"):
                _, coordinates = line.split(": ")
                x, y = map(lambda coord: coord[2:], coordinates.split(", "))  # Skip 'X=' or 'Y='
                prize = (int(x), int(y))

        return {'buttons': buttons, 'prize': prize}

    def min_button_presses(self, buttons, prize):
        target_x, target_y = prize
        dp = {}

        def dfs(current_x, current_y, total_tokens_spent, button_presses):
            if total_tokens_spent > 400:  # Assume max token limit of 200
                return None, {}
            if (current_x, current_y) == (target_x, target_y):
                return total_tokens_spent, button_presses
            if (current_x, current_y, total_tokens_spent) in dp:
                return dp[(current_x, current_y, total_tokens_spent)]

            min_tokens = None
            min_button_presses = {}

            for button, (bx, by) in buttons.items():
                new_x = current_x + bx
                new_y = current_y + by
                new_tokens_spent = total_tokens_spent + self.button_tokens[button]
                new_button_presses = button_presses.copy()
                new_button_presses[button] = new_button_presses.get(button, 0) + 1
                result, counts = dfs(new_x, new_y, new_tokens_spent, new_button_presses)

                if result is not None:
                    if min_tokens is None or result < min_tokens:
                        min_tokens = result
                        min_button_presses = counts

            dp[(current_x, current_y, total_tokens_spent)] = (min_tokens, min_button_presses)
            return min_tokens, min_button_presses

        result, button_counts = dfs(0, 0, 0, {})
        return sum(self.button_tokens[button] * count for button, count in button_counts.items()) if result else 0

    def min_button_presses_math(self, buttons, prize):
        target_x, target_y = prize
        dp = {}

        def dfs(current_x, current_y, total_tokens_spent, button_presses):
            if total_tokens_spent > 400:  # Assume max token limit of 200
                return None, {}
            if (current_x, current_y) == (target_x, target_y):
                return total_tokens_spent, button_presses
            if (current_x, current_y, total_tokens_spent) in dp:
                return dp[(current_x, current_y, total_tokens_spent)]

            min_tokens = None
            min_button_presses = {}

            for button, (bx, by) in buttons.items():
                new_x = current_x + bx
                new_y = current_y + by
                new_tokens_spent = total_tokens_spent + self.button_tokens[button]
                new_button_presses = button_presses.copy()
                new_button_presses[button] = new_button_presses.get(button, 0) + 1
                result, counts = dfs(new_x, new_y, new_tokens_spent, new_button_presses)

                if result is not None:
                    if min_tokens is None or result < min_tokens:
                        min_tokens = result
                        min_button_presses = counts

            dp[(current_x, current_y, total_tokens_spent)] = (min_tokens, min_button_presses)
            return min_tokens, min_button_presses

        result, button_counts = dfs(0, 0, 0, {})
        return sum(self.button_tokens[button] * count for button, count in button_counts.items()) if result else 0

    def min_squares(self, buttons, prize):
        from sympy import symbols, Eq, solve, core

        # the outer square we are going to try to fill
        outer_width = prize[0]
        outer_height = prize[1]

        # the inner squares we will fill it with
        square_a_width = buttons['Button A'][0]
        square_a_height = buttons['Button A'][1]
        square_a_weight = self.button_tokens['Button A']
        square_b_width = buttons['Button B'][0]
        square_b_height = buttons['Button B'][1]
        square_b_weight = self.button_tokens['Button B']

        square_a_presses, square_b_presses = symbols('square_a_presses square_b_presses')

        equation1 = Eq((square_a_presses * square_a_width) + (square_b_presses * square_b_width), outer_width)
        equation2 = Eq((square_a_presses * square_a_height) + (square_b_presses * square_b_height), outer_height)

        solution = solve((equation1, equation2), (square_a_presses, square_b_presses))

        if type(solution[square_a_presses]) == core.numbers.Integer and type(solution[square_b_presses]) == core.numbers.Integer:
            return solution[square_a_presses] * square_a_weight + solution[square_b_presses] * square_b_weight
        return 0

    def solve_part_one(self):
        # Assume that we will call min_button_presses with the relevant parsed data
        rv = 0
        for block in self.parsed_data:
            rv += self.min_squares(block['buttons'], block['prize'])
        return rv

    def solve_part_two(self):
        rv = 0
        for block in self.parsed_data:
            # Add 10000000000000 to the prize location before calling min_button_presses
            adjusted_prize = (block['prize'][0] + 10000000000000, block['prize'][1] + 10000000000000)
            rv += self.min_squares(block['buttons'], adjusted_prize)
        return rv
