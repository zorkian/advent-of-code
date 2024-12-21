from .day import Day


class Day21(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=21, use_test_data=use_test_data)

    def parse_input(self):
        self.parsed_data = [list(line) for line in self.input_data]
        self.numpad = {
            (0, 0): "7",
            (1, 0): "8",
            (2, 0): "9",
            (0, 1): "4",
            (1, 1): "5",
            (2, 1): "6",
            (0, 2): "1",
            (1, 2): "2",
            (2, 2): "3",
            (1, 3): "0",
            (2, 3): "A",
        }
        self.numpad_inverse = {v: k for k, v in self.numpad.items()}
        self.dirpad = {(1, 0): "^", (2, 0): "A", (0, 1): "<", (1, 1): "v", (2, 1): ">"}
        self.dirpad_inverse = {v: k for k, v in self.dirpad.items()}
        self.directions = {(0, -1): "^", (0, 1): "v", (-1, 0): "<", (1, 0): ">"}
        self.robots = [
            (2, 3, self.numpad, self.numpad_inverse),  # last robot on a numpad
            (2, 0, self.dirpad, self.dirpad_inverse),  # second robot
            (2, 0, self.dirpad, self.dirpad_inverse),  # third robot
            (2, 0, self.dirpad, self.dirpad_inverse), # human
        ]

    def bfs(self, start, goal, input_dict, memo):
        if (start, goal) in memo:
            return memo[(start, goal)]

        from collections import deque

        queue = deque([(start, [], {start})])
        min_length = float("inf")
        paths = []

        while queue:
            current, dirs, visited = queue.popleft()

            if current == goal:
                path_length = len(dirs)
                if path_length < min_length:
                    min_length = path_length
                    paths = [dirs]
                elif path_length == min_length:
                    paths.append(dirs)
                continue

            for direction in self.directions.keys():
                next_pos = (current[0] + direction[0], current[1] + direction[1])
                if next_pos in input_dict and next_pos not in visited:
                    nvisited = visited.copy()
                    nvisited.add(next_pos)
                    ndirs = dirs.copy()
                    ndirs.append(self.directions[direction])
                    queue.append((next_pos, ndirs, nvisited))

        if not paths:
            raise Exception("unreachable somehow")

        memo[(start, goal)] = paths
        return paths

    def process_char(self, robots, char, memo):
        # if we have no robots, we're done
        if len(robots) <= 1:
            return 1

        # return memoized version, which is the shortest path given how
        # many robots are left and the current character
        position, input_dict = (robots[0][0], robots[0][1]), robots[0][2]
        mkey = (len(robots), position, char)
        if mkey in memo:
            return memo[mkey]

        # no memoization here, so we have to calculate the shortest path
        # for us to get to the character
        goal_position = next(
            (pos for pos, value in input_dict.items() if value == char), None
        )
        if not goal_position:
            raise Exception("no goal position")

        # we're already in position (A) so just press it
        if position == goal_position:
            return 1

        # get all possible paths to get to this location
        directions = {
            path: 0
            for path in [
                "".join(d) + "A"
                for d in self.bfs(position, goal_position, input_dict, memo)
            ]
        }

        # iterate each path, find the shortest sum
        startpos = robots[1][3]['A']
        for path in directions:
            for pathchar in path:
                robots[1] = (startpos[0], startpos[1], robots[1][2], robots[1][3])
                directions[path] += self.process_char(robots[1:], pathchar, memo)
                startpos = robots[1][3][pathchar]
        # print(mkey, ' :: ', directions)

        # find shortest path, memo, return
        robots[0] = (goal_position[0], goal_position[1], robots[0][2])
        shortest = min(directions.values())
        memo[mkey] = shortest
        return shortest

    def solve_part_one(self):
        rv = 0
        for code in self.parsed_data:
            memo = {}
            shortest = 0
            for char in code:
                shortest += self.process_char(self.robots, char, memo)

            #shortest = self.process_goal_string(self.robots, code, memo)
            val = int("".join(filter(lambda x: x.isdigit(), code)))
            # print(f"Code: {code}, Value: {val}, Len: {shortest}")
            rv += val * shortest
        return rv

    def solve_part_two(self):
        self.robots = [
            (2, 3, self.numpad, self.numpad_inverse),  # last robot on a numpad
            (2, 0, self.dirpad, self.dirpad_inverse),  # 1
            (2, 0, self.dirpad, self.dirpad_inverse),  # 2
            (2, 0, self.dirpad, self.dirpad_inverse),  # 3
            (2, 0, self.dirpad, self.dirpad_inverse),  # 4
            (2, 0, self.dirpad, self.dirpad_inverse),  # 5
            (2, 0, self.dirpad, self.dirpad_inverse),  # 1
            (2, 0, self.dirpad, self.dirpad_inverse),  # 2
            (2, 0, self.dirpad, self.dirpad_inverse),  # 3
            (2, 0, self.dirpad, self.dirpad_inverse),  # 4
            (2, 0, self.dirpad, self.dirpad_inverse),  # 5
            (2, 0, self.dirpad, self.dirpad_inverse),  # 1
            (2, 0, self.dirpad, self.dirpad_inverse),  # 2
            (2, 0, self.dirpad, self.dirpad_inverse),  # 3
            (2, 0, self.dirpad, self.dirpad_inverse),  # 4
            (2, 0, self.dirpad, self.dirpad_inverse),  # 5
            (2, 0, self.dirpad, self.dirpad_inverse),  # 1
            (2, 0, self.dirpad, self.dirpad_inverse),  # 2
            (2, 0, self.dirpad, self.dirpad_inverse),  # 3
            (2, 0, self.dirpad, self.dirpad_inverse),  # 4
            (2, 0, self.dirpad, self.dirpad_inverse),  # 5
            (2, 0, self.dirpad, self.dirpad_inverse),  # 1
            (2, 0, self.dirpad, self.dirpad_inverse),  # 2
            (2, 0, self.dirpad, self.dirpad_inverse),  # 3
            (2, 0, self.dirpad, self.dirpad_inverse),  # 4
            (2, 0, self.dirpad, self.dirpad_inverse),  # 5
            (2, 0, self.dirpad, self.dirpad_inverse),  # human
        ]

        rv = 0
        for code in self.parsed_data:
            memo = {}
            shortest = 0
            for char in code:
                shortest += self.process_char(self.robots, char, memo)

            #shortest = self.process_goal_string(self.robots, code, memo)
            val = int("".join(filter(lambda x: x.isdigit(), code)))
            # print(f"Code: {code}, Value: {val}, Len: {shortest}")
            rv += val * shortest
        return rv
