from .day import Day


class Day6(Day):
    def __init__(self, use_test_data=False):
        self.map = []
        self.visited = {}
        self.starting_location = None
        self.starting_char = None
        super().__init__(day_number=6, use_test_data=use_test_data)

    def parse_input(self):
        for y, line in enumerate(self.input_data):
            row = []
            for x, char in enumerate(line):
                if char in "><^v":  # Check for starting location
                    self.starting_location = (x, y)
                    self.starting_char = char
                    char = '.'  # Replace starting location character with a period
                row.append(char)
                self.visited[(x, y)] = []  # Initialize visited directions for each location
            self.map.append(row)

    def print_map(self, x, y):
        """Print the current state of the map with the guard's position and visited paths."""
        if self.use_test_data:  # Only print the map if using test data
            for row_index, row in enumerate(self.map):
                printed_row = []
                for col_index, char in enumerate(row):
                    if (col_index, row_index) == (x, y):
                        printed_row.append('G')  # Mark guard's current position
                    elif (col_index, row_index) in self.visited:
                        printed_row.append('*')  # Mark visited path
                    else:
                        printed_row.append(char)  # Print normal map character
                print(''.join(printed_row))
            print()  # New line for better readability

    def solve_part_one(self):
        self.visited = {}
        direction_map = {
            '>': (1, 0),
            '<': (-1, 0),
            '^': (0, -1),
            'v': (0, 1)
        }
        directions = ['>', 'v', '<', '^']  # Right turn sequence
        current_direction = self.starting_char
        x, y = self.starting_location

        if current_direction is None:
            return 0  # Exit if starting direction is invalid

        while 0 <= y < len(self.map) and 0 <= x < len(self.map[0]):
            self.visited[(x, y)] = True  # Mark the current location as visited

            dx, dy = direction_map[current_direction]
            next_x, next_y = x + dx, y + dy

            if 0 <= next_y < len(self.map) and 0 <= next_x < len(self.map[0]):
                if self.map[next_y][next_x] == '.':  # Move to empty square
                    x, y = next_x, next_y
                elif self.map[next_y][next_x] == '#':  # Rotate right on hitting an obstacle
                    current_direction = directions[(directions.index(current_direction) + 1) % 4]
                    # Do not change x, y; just rotate
            else:
                break  # Walks off the map

        visited_count = sum(self.visited.values())
        return visited_count  # Return the number of visited locations

    def solve_part_two(self):
        infinite_loop_count = 0
        direction_map = {
            '>': (1, 0),
            '<': (-1, 0),
            '^': (0, -1),
            'v': (0, 1)
        }

        # Create a set of the locations visited during the guard's path
        path_locations = set()
        direction = self.starting_char
        x, y = self.starting_location

        while 0 <= y < len(self.map) and 0 <= x < len(self.map[0]):
            path_locations.add((x, y))
            dx, dy = direction_map[direction]
            next_x, next_y = x + dx, y + dy

            if 0 <= next_y < len(self.map) and 0 <= next_x < len(self.map[0]):
                if self.map[next_y][next_x] == '.':
                    x, y = next_x, next_y
                elif self.map[next_y][next_x] == '#':
                    direction = self.rotate_right(direction)
            else:
                break  # Walks off the map

        # Only place obstacles at the locations on the default path
        for (x, y) in path_locations:
            if self.map[y][x] == '.':  # Only place obstacles in free squares
                self.map[y][x] = '#'  # Place an obstacle
                if self.check_for_infinite_loop(x, y, direction_map):
                    infinite_loop_count += 1
                self.map[y][x] = '.'  # Remove the obstacle

        return infinite_loop_count  # Return the number of infinite loops found

    def check_for_infinite_loop(self, start_x, start_y, direction_map):
        visited = set()
        current_direction = self.starting_char
        x, y = self.starting_location

        while 0 <= y < len(self.map) and 0 <= x < len(self.map[0]):
            if (x, y, current_direction) in visited:
                return True  # Infinite loop detected
            visited.add((x, y, current_direction))

            dx, dy = direction_map[current_direction]
            next_x, next_y = x + dx, y + dy

            if 0 <= next_y < len(self.map) and 0 <= next_x < len(self.map[0]):
                if self.map[next_y][next_x] == '.':
                    x, y = next_x, next_y
                elif self.map[next_y][next_x] == '#':
                    # Rotate right on hitting an obstacle
                    current_direction = self.rotate_right(current_direction)
            else:
                break  # Walks off the map

        return False  # No infinite loop detected

    def rotate_right(self, direction):
        return {
            '>': 'v',
            'v': '<',
            '<': '^',
            '^': '>'
        }[direction]
