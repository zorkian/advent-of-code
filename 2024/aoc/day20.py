from .day import Day
from collections import deque


class Day20(Day):
    def __init__(self, use_test_data=False):
        self.map = {}
        self.start = None
        self.end = None
        super().__init__(day_number=20, use_test_data=use_test_data)

    def parse_input(self):
        for y, line in enumerate(self.input_data):
            for x, char in enumerate(line):
                if char in (".", "#"):
                    self.map[(x, y)] = char
                elif char == "S":
                    self.start = (x, y)
                    self.map[(x, y)] = "."
                elif char == "E":
                    self.end = (x, y)
                    self.map[(x, y)] = "."


    def find_shortest_path(self, enable_wall_hack=True, forbidden_walls=None):
        if not self.start or not self.end:
            return -1, None

        if forbidden_walls is None:
            forbidden_walls = []

        queue = deque(
            [(self.start, 0, False, None)]
        )  # ((x, y), distance, used_wall, hacked_wall)
        visited = {(self.start, False)}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        while queue:
            (current_x, current_y), distance, used_wall, hacked_wall = queue.popleft()

            if (current_x, current_y) == self.end:
                return distance, hacked_wall

            for dx, dy in directions:
                neighbor = (current_x + dx, current_y + dy)
                if neighbor in self.map:
                    if (
                        self.map[neighbor] == "."
                        and (neighbor, used_wall) not in visited
                    ):
                        visited.add((neighbor, used_wall))
                        queue.append((neighbor, distance + 1, used_wall, hacked_wall))
                    elif (
                        self.map[neighbor] == "#"
                        and not used_wall
                        and enable_wall_hack
                        and neighbor not in forbidden_walls
                    ):
                        visited.add((neighbor, True))
                        queue.append((neighbor, distance + 1, True, neighbor))

        return -1, None  # If no path is found

    def memoized_shortest_path(self, start_x, start_y, memo):
        if (start_x, start_y) in memo:
            return memo[(start_x, start_y)]

        queue = deque([self.end])  # Start from the initial position
        memo[self.end] = 0  # The distance to end itself is 0

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        while queue:
            current_x, current_y = queue.popleft()

            if (current_x, current_y) == (start_x, start_y):
                return memo[(current_x, current_y)]

            for dx, dy in directions:
                neighbor = (current_x + dx, current_y + dy)
                if neighbor in self.map and self.map[neighbor] == ".":
                    new_distance = memo[(current_x, current_y)] + 1
                    if neighbor not in memo or new_distance < memo[neighbor]:
                        memo[neighbor] = new_distance
                        queue.append(neighbor)

        return -1  # If no path is found

    def find_shortest_path_with_timeskip(self, max_timeskip=None):
        if not self.start or not self.end:
            return -1, None

        memo = {}
        timeskips = set()  # timeskips that save time 100 units of time
        timeskips_by_savings = {}
        queue = deque([(self.start, 0)])  # ((x, y), distance)
        visited = {self.start}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        while queue:
            (current_x, current_y), distance = queue.popleft()

            if (current_x, current_y) == self.end:
                #for savings in sorted(timeskips_by_savings.keys()):
                    #print(
                    #    f"Timeskips saving {savings}: {timeskips_by_savings[savings]}"
                    #)
                return distance, len(timeskips)

            # We are at a new square, find all the non-wall coordinates within the timeskip
            # range and calculate the possible time savings by using any that make the path
            # shorter for us (I don't think we need to prune out visited spots already because
            # they should be guaranteed to be longer?)
            for coord in self.get_non_wall_coordinates(
                current_x, current_y, max_timeskip
            ):
                if coord in visited:
                    continue
                possible_savings = (
                    self.memoized_shortest_path(current_x, current_y, memo)
                    - self.memoized_shortest_path(coord[0], coord[1], memo)
                    - (abs(current_x - coord[0]) + abs(current_y - coord[1]))
                )
                if possible_savings < 100:
                    continue
                #print(
                #    f"Possible savings: {current_x, current_y} -> {coord} saves {possible_savings}"
                #)
                timeskips.add((current_x, current_y, coord[0], coord[1]))
                if possible_savings not in timeskips_by_savings:
                    timeskips_by_savings[possible_savings] = set()
                timeskips_by_savings[possible_savings].add(
                    (current_x, current_y, coord[0], coord[1])
                )

            for dx, dy in directions:
                neighbor = (current_x + dx, current_y + dy)
                if (
                    neighbor in self.map
                    and self.map[neighbor] == "."
                    and neighbor not in visited
                ):
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))

        return -1, 0  # If no path is found

    def get_non_wall_coordinates(self, start_x, start_y, max_distance):
        non_wall_coords = []
        for x in range(start_x - max_distance, start_x + max_distance + 1):
            for y in range(start_y - max_distance, start_y + max_distance + 1):
                if abs(x - start_x) + abs(y - start_y) <= max_distance:
                    if (x, y) in self.map and self.map[(x, y)] != "#":
                        non_wall_coords.append((x, y))
        return non_wall_coords

    def solve_part_one(self):
        _, count = self.find_shortest_path_with_timeskip(2)
        return count

    def solve_part_two(self):
        _, count = self.find_shortest_path_with_timeskip(20)
        return count
