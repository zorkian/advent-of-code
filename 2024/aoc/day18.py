from .day import Day
from collections import deque


class Day18(Day):
    def __init__(self, use_test_data=False):
        self.coordinates = {}
        self.coords_by_time = {}
        self.width = 7 if use_test_data else 71
        self.height = 7 if use_test_data else 71
        self.max_time = 12 if use_test_data else 1024
        super().__init__(day_number=18, use_test_data=use_test_data)

    def parse_input(self):
        for line_number, line in enumerate(self.input_data):
            x, y = map(int, line.split(","))
            self.coordinates[(x, y)] = line_number
            self.end_time = line_number
            self.coords_by_time[line_number] = (x, y)

    def shortest_path(self, start, end, max_line_number=None):
        if start in self.coordinates or end in self.coordinates:
            return None

        queue = deque([(start, 0)])  # (current position, path length)
        visited = set()
        visited.add(start)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        while queue:
            current, path_length = queue.popleft()
            if current == end:
                return path_length

            for direction in directions:
                next_x = current[0] + direction[0]
                next_y = current[1] + direction[1]
                next_coordinate = (next_x, next_y)

                if (
                    0 <= next_x < self.width
                    and 0 <= next_y < self.height
                    and (
                        next_coordinate not in self.coordinates
                        or (
                            max_line_number is not None
                            and self.coordinates[next_coordinate] >= max_line_number
                        )
                    )
                    and next_coordinate not in visited
                ):
                    visited.add(next_coordinate)
                    queue.append((next_coordinate, path_length + 1))

        return None  # No path found

    def solve_part_one(self):
        start = (0, 0)  # Assuming starting point is (0, 0)
        end = (
            self.width - 1,
            self.height - 1,
        )  # Assuming end point is bottom-right corner
        return self.shortest_path(start, end, max_line_number=self.max_time)

    def solve_part_two(self):
        start = (0, 0)  # Assuming starting point is (0, 0)
        end = (
            self.width - 1,
            self.height - 1,
        )  # Assuming end point is bottom-right corner
        for i in range(1024, self.end_time):
            pl = self.shortest_path(start, end, max_line_number=i)
            if pl is None:
                print(f"Part two real: {','.join(map(str, self.coords_by_time[i-1]))}")
                return 0
