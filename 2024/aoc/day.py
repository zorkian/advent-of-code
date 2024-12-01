class Day:
    def __init__(self, day_number, use_test_data=False):
        self.day_number = day_number
        self.input_data = []
        self.use_test_data = use_test_data
        self.read_input()
        self.parse_input()

    def read_input(self):
        file_path = (
            f"inputs/day{self.day_number}.test"
            if self.use_test_data
            else f"inputs/day{self.day_number}.data"
        )

        try:
            with open(file_path, "r") as f:
                self.input_data = (
                    f.read().strip().split("\n")
                )  # Read and automatically parse into a list
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def parse_input(self):
        # Override this method in subclasses to parse input data
        pass

    def part_one(self):
        print(f"Part one: {self.solve_part_one()}")

    def solve_part_one(self) -> int:
        # Override this method in subclasses to solve part one
        raise NotImplementedError

    def part_two(self):
        print(f"Part two: {self.solve_part_two()}")

    def solve_part_two(self) -> int:
        # Override this method in subclasses to solve part two
        raise NotImplementedError
