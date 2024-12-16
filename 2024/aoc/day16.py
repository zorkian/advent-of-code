from .day import Day

from collections import deque

class Day16(Day):
    def __init__(self, use_test_data=False):
        self.graph = {}
        self.start_node = None
        self.terminal_node = None
        super().__init__(day_number=16, use_test_data=use_test_data)

    def parse_input(self):
        # First phase: parse out all locations
        for y, line in enumerate(self.input_data):
            for x, char in enumerate(line):
                if char == '#':
                    continue
                elif char == 'S':
                    self.start_node = (x, y)
                elif char == 'E':
                    self.terminal_node = (x, y)

                self.graph[(x, y)] = {
                    'location': (x, y),
                    'connections': {}
                }

        # Second phase: establish connections
        for (x, y), data in self.graph.items():
            if (x > 0) and ((x - 1, y) in self.graph):
                self.graph[(x, y)]['connections']['left'] = (x - 1, y)
            if (x < len(self.input_data[y]) - 1) and ((x + 1, y) in self.graph):
                self.graph[(x, y)]['connections']['right'] = (x + 1, y)
            if (y > 0) and ((x, y - 1) in self.graph):
                self.graph[(x, y)]['connections']['up'] = (x, y - 1)
            if (y < len(self.input_data) - 1) and ((x, y + 1) in self.graph):
                self.graph[(x, y)]['connections']['down'] = (x, y + 1)

    def find_all_paths(self, of_cost=None):
        directions = ['right', 'down', 'left', 'up']
        queue = deque([(self.start_node, 0, 'right', set())])  # (current_position, total_cost, current_direction, visited_nodes)
        all_paths = []
        memo = {}  # To store the results of visited positions with their corresponding total cost and entry direction

        while queue:
            current_position, total_cost, current_direction, visited_nodes = queue.popleft()
            visited_nodes.add(current_position)

            if current_position == self.terminal_node:
                #print(f"Found path with cost {total_cost} and visited nodes {visited_nodes}")
                all_paths.append((total_cost, list(visited_nodes)))  # Store the total cost of this path
                continue  # Continue to find other paths

            # Check if current_position has been visited from the same direction with a less costly path
            if True or of_cost is None:
                if (current_position, current_direction) in memo and memo[(current_position, current_direction)] < total_cost:
                    continue  # Skip this path if it wasn't better than previously found
                # Update the memoization with the current position and cost
                memo[(current_position, current_direction)] = total_cost

            for direction, (dx, dy) in zip(directions, [(1, 0), (0, 1), (-1, 0), (0, -1)]):
                next_position = (current_position[0] + dx, current_position[1] + dy)

                if next_position in self.graph and next_position not in visited_nodes:
                    new_cost = total_cost + 1  # Step forward is always 1 point
                    if direction != current_direction:  # Only add rotation cost if direction has changed
                        new_cost += 1000

                    # if cost has exceeded, throw away this path
                    if of_cost is not None and new_cost > of_cost:
                        #print(f"Path cost exceeded {of_cost} at {next_position}")
                        continue

                    queue.append((next_position, new_cost, direction, visited_nodes.copy()))  # Pass a copy of visited_nodes to avoid mutation

        return all_paths

    def find_shortest_path(self, start, end):
        # If no paths found, return infinity. Otherwise, return the shortest path cost.
        all_paths = self.find_all_paths()
        if all_paths:
            shortest_path = min(all_paths, key=lambda x: x[0])
            #print(all_paths)
            unique_locations = set()
            for path in all_paths:
                if path[0] == shortest_path[0]:
                    for p in path[1]:
                        unique_locations.add(p)
            self.print_maze_path(list(unique_locations))
            # self.print_maze_path(shortest_path[1])  # Print the maze path at the end
            return shortest_path[0] # Return cost and count of unique locations
        return float('inf')  # If no path is found

    def print_maze_path(self, path):
        maze = [[' ' for _ in range(len(self.input_data[0]))] for _ in range(len(self.input_data))]
        for (x, y) in self.graph.keys():
            if (x, y) == self.start_node:
                maze[y][x] = 'S'  # Start node
            elif (x, y) == self.terminal_node:
                maze[y][x] = 'E'  # End node
            else:
                maze[y][x] = '.'  # Free space

        for i in range(len(path)):
            current = path[i]  # Get the position from the path to mark
            maze[current[1]][current[0]] = '*'  # Mark the path

        for line in maze:
            print(''.join(line))  # Print the maze

    def solve_part_one(self):
        return self.find_shortest_path(self.start_node, self.terminal_node)

    def solve_part_two(self):
        all_paths = self.find_all_paths(of_cost=self.find_shortest_path(self.start_node, self.terminal_node))
        uniqs = set()
        for path in all_paths:
            for p in path[1]:
                uniqs.add(p)
        return len(uniqs)
