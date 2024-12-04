from .day import Day


class Day4(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=4, use_test_data=use_test_data)

    def parse_input(self):
        self.data_grid = [list(line) for line in self.input_data]

    def count_sequences(self, sequence):
        count = 0

        # Check horizontal and inverted horizontal
        for row in self.data_grid:
            row_str = ''.join(row)
            count += row_str.count(sequence)
            count += row_str.count(sequence[::-1])

        # Check vertical and inverted vertical
        for col in range(len(self.data_grid[0])):
            col_str = ''.join(row[col] for row in self.data_grid)
            count += col_str.count(sequence)
            count += col_str.count(sequence[::-1])

        # Check diagonals and inverted diagonals
        diagonals = self.get_diagonals()
        for diag in diagonals:
            diag_str = ''.join(diag)
            count += diag_str.count(sequence)
            count += diag_str.count(sequence[::-1])

        return count

    def get_diagonals(self):
        diagonals = []
        height = len(self.data_grid)
        width = len(self.data_grid[0])

        # Get diagonals from the top-left to bottom-right
        for r in range(height):
            diag = []
            for d in range(min(width, height - r)):
                diag.append(self.data_grid[r + d][d])
            diagonals.append(diag)

        for c in range(1, width):
            diag = []
            for d in range(min(height, width - c)):
                diag.append(self.data_grid[d][c + d])
            diagonals.append(diag)

        # Get diagonals from the top-right to bottom-left
        for r in range(height):
            diag = []
            for d in range(min(width, height - r)):
                diag.append(self.data_grid[r + d][width - 1 - d])
            diagonals.append(diag)

        for c in range(width - 2, -1, -1):
            diag = []
            for d in range(min(height, c + 1)):
                diag.append(self.data_grid[d][c - d])
            diagonals.append(diag)

        return diagonals

    def solve_part_one(self):
        return self.count_sequences("XMAS")

    def solve_part_two(self):
        count = 0

        # Check diagonals for sequences "SAM" and "MAS"
        for r in range(1, len(self.data_grid) - 1):
            for c in range(1, len(self.data_grid[0]) - 1):
                if self.data_grid[r][c] == 'A':
                    # Check for diagonal sequences (up-left to down-right)
                    diag_lr = (self.data_grid[r - 1][c - 1], self.data_grid[r][c], self.data_grid[r + 1][c + 1])
                    diag_rl = (self.data_grid[r - 1][c + 1], self.data_grid[r][c], self.data_grid[r + 1][c - 1])

                    if (diag_lr == ('S', 'A', 'M') or diag_lr == ('M', 'A', 'S')) and \
                    (diag_rl == ('S', 'A', 'M') or diag_rl == ('M', 'A', 'S')):
                        count += 1

        return count
