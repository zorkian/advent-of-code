from .day import Day
from collections import namedtuple


class Day14(Day):
    Robot = namedtuple('Robot', ['position', 'velocity'])

    def __init__(self, use_test_data=False):
        if use_test_data:
            self.width = 11
            self.height = 7
        else:
            self.width = 101
            self.height = 103
        self.robots = []
        super().__init__(day_number=14, use_test_data=use_test_data)

    def parse_input(self):
        for line in self.input_data:
            position_part, velocity_part = line.split(' ')
            p = tuple(map(int, position_part.split('=')[1].split(',')))
            v = tuple(map(int, velocity_part.split('=')[1].split(',')))
            self.robots.append(self.Robot(position=p, velocity=v))

    def simulate_turns(self, n):
        for i, robot in enumerate(self.robots):
            new_x = (robot.position[0] + (robot.velocity[0] * n)) % self.width
            new_y = (robot.position[1] + (robot.velocity[1] * n)) % self.height
            self.robots[i] = self.Robot(position=(new_x, new_y), velocity=robot.velocity)

    def solve_part_one(self):
        self.simulate_turns(100)

        top_left = 0
        top_right = 0
        bottom_left = 0
        bottom_right = 0

        mid_x = self.width // 2
        mid_y = self.height // 2

        for robot in self.robots:
            x, y = robot.position
            if x == mid_x or y == mid_y:
                continue  # Ignore robots in the middle

            if x < mid_x and y < mid_y:
                top_left += 1
            elif x >= mid_x and y < mid_y:
                top_right += 1
            elif x < mid_x and y >= mid_y:
                bottom_left += 1
            elif x >= mid_x and y >= mid_y:
                bottom_right += 1

        score = top_left * top_right * bottom_left * bottom_right
        return score

    def solve_part_two(self):
        count = 100 # already ran 100 on part one lol
        while True:
            # Check for at least 10 stars next to each other in row 28
            row_28 = [robot.position[0] for robot in self.robots if robot.position[1] == 28]
            if self.has_consecutive_stars(row_28, 10):
                #print()
                #self.print_field()
                break

            count += 1
            self.simulate_turns(1)

        return count

    def has_consecutive_stars(self, positions, target_streak):
        if not positions:
            return False
        positions = sorted(set(positions))
        current_streak = 1
        for i in range(1, len(positions)):
            if positions[i] == positions[i - 1] + 1:
                current_streak += 1
                if current_streak >= target_streak:
                    return True
            else:
                current_streak = 1
        return False

    def print_field(self):
        field = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for robot in self.robots:
            x, y = robot.position
            field[y][x] = '*'
        ct = 0
        for row in field:
            print(str(ct) + ' ' + ''.join(row))
            ct += 1
