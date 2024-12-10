from .day import Day


class Day10(Day):
    def __init__(self, use_test_data=False, debug=False):
        self.debug = debug
        self.trees = []
        self.grid = []  # 2D structure to hold the parsed input data
        self.paths_by_origin = {}  # To store unique destinations for each origin
        self.paths_by_origin_p1 = {}  # To store unique destinations for each origin
        super().__init__(day_number=10, use_test_data=use_test_data)

    def parse_input(self):
        self.grid = [list(line) for line in self.input_data]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == '0':
                    unique_paths = self.count_unique_paths(x, y)  # Store the unique destinations for each origin
                    self.paths_by_origin[(x, y)] = unique_paths
                    self.paths_by_origin_p1[(x, y)] = self.build_tree(x, y)  # Store the unique destinations for each origin
                    if self.debug:
                        print(f"Processed origin ({x}, {y}) with unique paths: {unique_paths}")

    def build_tree(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
        unique_destinations = set()  # To store unique destinations for the current origin

        def traverse_path(x, y, current_length, path):
            if current_length == 10:  # We have a complete path from 0 to 9
                unique_destinations.add(path[-1])  # Add the end point of the path as a unique destination
                return

            current_value = int(self.grid[y][x])
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    if int(self.grid[ny][nx]) == current_value + 1:  # Go to the next number
                        traverse_path(nx, ny, current_length + 1, path + [(nx, ny)])

        traverse_path(x, y, 1, [(x, y)])  # Start with the initial "0" in the path
        return unique_destinations  # Return the set of unique destinations

    def count_unique_paths(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
        unique_path_count = 0  # To store the count of unique paths for the current origin

        def traverse_path(x, y, current_length):
            nonlocal unique_path_count
            if current_length == 10:  # We have a complete path from 0 to 9
                unique_path_count += 1  # Count this valid unique path
                return

            current_value = int(self.grid[y][x])
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    if int(self.grid[ny][nx]) == current_value + 1:  # Go to the next number
                        traverse_path(nx, ny, current_length + 1)

        traverse_path(x, y, 1)  # Start with the initial "0" in the path
        return unique_path_count  # Return the count of unique paths

    def count_all_paths(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
        path_count = 0  # To store the total count of paths for the current origin

        def traverse_path(x, y, current_length):
            nonlocal path_count
            if current_length == 10:  # This includes the complete path from 0 to 9
                path_count += 1  # Count this valid path
                return

            current_value = int(self.grid[y][x])
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    if int(self.grid[ny][nx]) == current_value + 1:  # Go to the next number
                        traverse_path(nx, ny, current_length + 1)

        traverse_path(x, y, 1)  # Start with the initial "0" in the path
        return path_count  # Return the total count of paths

    def solve_part_one(self):
        total_unique_paths = sum(len(destinations) for destinations in self.paths_by_origin_p1.values())
        return total_unique_paths

    def solve_part_two(self):
        total_paths = sum(self.count_all_paths(x, y) for (x, y) in self.paths_by_origin)
        return total_paths
