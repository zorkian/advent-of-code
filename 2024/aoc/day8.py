from .day import Day


class Day8(Day):
    def __init__(self, use_test_data=False, debug=False):
        self.max_width = 0
        self.max_height = 0
        self.debug = debug
        super().__init__(day_number=8, use_test_data=use_test_data)

    def parse_input(self):
        self.symbol_locations = {}
        for y, line in enumerate(self.input_data):
            self.max_height = max(self.max_height, y + 1)
            self.max_width = max(self.max_width, len(line))
            for x, char in enumerate(line):
                if char != '.':
                    if char not in self.symbol_locations:
                        self.symbol_locations[char] = []
                    self.symbol_locations[char].append((x, y))

    def calculate_antinodes(self):
        symbols = list(self.symbol_locations.keys())
        unique_points = set()  # Use a set to track unique points
        grid = [['.' for _ in range(self.max_width)] for _ in range(self.max_height)]  # Initialize the grid

        for symbol in symbols:
            locations = self.symbol_locations[symbol]
            # Place the symbol in the grid
            for (x, y) in locations:
                grid[y][x] = symbol

            # Generate all unique pairs of locations
            location_pairs = [(loc_a, loc_b) for i, loc_a in enumerate(locations) for loc_b in locations[i + 1:]]
            for (bx, by), (cx, cy) in location_pairs:
                delta_x = cx - bx
                delta_y = cy - by
                ax, ay = bx - delta_x, by - delta_y
                dx, dy = cx + delta_x, cy + delta_y

                # Ensure points A and D are within the grid bounds
                if 0 <= ax < self.max_width and 0 <= ay < self.max_height:
                    unique_points.add((ax, ay))  # Add point A
                    grid[ay][ax] = '#'  # Mark point A as an antinode
                    if self.debug:
                        print(f"Adding unique point A: ({ax}, {ay}) for symbol '{symbol}'")  # Debug info for point A

                if 0 <= dx < self.max_width and 0 <= dy < self.max_height:
                    unique_points.add((dx, dy))  # Add point D
                    grid[dy][dx] = '#'  # Mark point D as an antinode
                    if self.debug:
                        print(f"Adding unique point D: ({dx}, {dy}) for symbol '{symbol}'")  # Debug info for point D

        # Print the grid
        if self.debug:
            for row in grid:
                print(''.join(row))

        return len(unique_points)  # Return the count of unique points created

    def calculate_antinodes_extended(self):
        symbols = list(self.symbol_locations.keys())
        unique_points = set()  # Use a set to track unique points
        grid = [['.' for _ in range(self.max_width)] for _ in range(self.max_height)]  # Initialize the grid

        for symbol in symbols:
            locations = self.symbol_locations[symbol]
            # Place the symbol in the grid
            for (x, y) in locations:
                grid[y][x] = symbol

            # Generate all unique pairs of locations
            location_pairs = [(loc_a, loc_b) for i, loc_a in enumerate(locations) for loc_b in locations[i + 1:]]
            for (bx, by), (cx, cy) in location_pairs:
                delta_x = cx - bx
                delta_y = cy - by

                # Extend line in the negative direction
                ax, ay = bx, by
                while 0 <= ax < self.max_width and 0 <= ay < self.max_height:
                    unique_points.add((ax, ay))
                    grid[ay][ax] = '#'
                    ax -= delta_x
                    ay -= delta_y

                # Extend line in the positive direction
                dx, dy = cx, cy
                while 0 <= dx < self.max_width and 0 <= dy < self.max_height:
                    unique_points.add((dx, dy))
                    grid[dy][dx] = '#'
                    dx += delta_x
                    dy += delta_y

        # Print the grid
        if self.debug:
            for row in grid:
                print(''.join(row))

        return len(unique_points)  # Return the count of unique points created

    def solve_part_one(self):
        return self.calculate_antinodes()

    def solve_part_two(self):
        return self.calculate_antinodes_extended()
