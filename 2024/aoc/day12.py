from .day import Day

import itertools


class Day12(Day):
    def __init__(self, use_test_data=False):
        self.coordinates = {}
        self.visited = set()
        super().__init__(day_number=12, use_test_data=use_test_data)

    def parse_input(self):
        for y, line in enumerate(self.input_data):
            for x, char in enumerate(line):
                self.coordinates[(x, y)] = char

    def flood_fill(self, start):
        stack = [start]
        char_type = self.coordinates[start]
        region_size = 0
        fencing_needed = 0
        region_coordinates = []

        while stack:
            x, y = stack.pop()
            if (x, y) in self.visited:
                continue
            self.visited.add((x, y))
            region_size += 1
            region_coordinates.append((x, y))

            # Check 4 directions (up, down, left, right) for fencing count
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in self.coordinates:
                    if neighbor not in self.visited:
                        if self.coordinates[neighbor] == char_type:
                            stack.append(neighbor)
                    if self.coordinates[neighbor] != char_type:
                        fencing_needed += 1
                else:
                    fencing_needed += 1

        return [region_coordinates, region_size, fencing_needed]

    def solve_part_one(self):
        price = 0
        for coordinate in self.coordinates:
            if coordinate not in self.visited:
                _, region_size, fencing_needed = self.flood_fill(coordinate)
                price += region_size * fencing_needed
        return price

    def count_sides(self, coords):
        # find a corner coordinate, direction is up/right/down/left
        # starting from 0
        start, direction = None, 0

        for coord in coords:
            #print(f"Coord: {coord}")
            x, y = coord
            if (x - 1, y) not in coords and (x - 1, y - 1) not in coords:
                # nothing to the left or up, so we're a top left corner
                # which means we can start by going right and be guaranteed
                # we're at the beginning of a rightward walk
                start = (x, y)
                direction = 1
                break
        if start is None:
            raise Exception("oh no, mark AI didn't work")

        # print(f"Start: {start} and Direction: {direction}")

        # now we walk around the region, counting the sides, turning right whenever
        # we can't go the direction anymore and stopping when we reach the start again
        current, corner_count = start, 1
        while True:
            if current == start and direction == 0:
                break

            x, y = current
            # print(f"Current: {current} Direction: {direction} Corner Count: {corner_count}")

            # going up
            if direction == 0:
                # going up, we can either go left, up, or right depending on the shape
                # of the piece
                if (x - 1, y - 1) in coords:
                    # going to the left
                    current = (x - 1, y - 1)
                    direction = 3
                    corner_count += 1
                elif (x, y - 1) in coords:
                    # continuing straight up
                    current = (x, y - 1)
                else:
                    # going right, but don't pick a new location, we're just rounding
                    # the top edge of this piece
                    corner_count += 1
                    direction = 1

            # going right
            elif direction == 1:
                # going right, we can either go up, right, or down depending on the shape
                # of the piece
                if (x + 1, y - 1) in coords:
                    # going up
                    current = (x + 1, y - 1)
                    direction = 0
                    corner_count += 1
                elif (x + 1, y) in coords:
                    # continuing straight right
                    current = (x + 1, y)
                else:
                    # going down, but don't pick a new location, we're just rounding
                    # the right edge of this piece
                    corner_count += 1
                    direction = 2

            # going down
            elif direction == 2:
                # going down, we can either go right, down, or left depending on the shape
                # of the piece
                if (x + 1, y + 1) in coords:
                    # going right
                    current = (x + 1, y + 1)
                    direction = 1
                    corner_count += 1
                elif (x, y + 1) in coords:
                    # continuing straight down
                    current = (x, y + 1)
                else:
                    # going left, but don't pick a new location, we're just rounding
                    # the bottom edge of this piece
                    corner_count += 1
                    direction = 3

            # going left
            elif direction == 3:
                # going left, we can either go down, left, or up depending on the shape
                # of the piece
                if (x - 1, y + 1) in coords:
                    # going down
                    current = (x - 1, y + 1)
                    direction = 2
                    corner_count += 1
                elif (x - 1, y) in coords:
                    # continuing straight left
                    current = (x - 1, y)
                else:
                    # going up, but don't pick a new location, we're just rounding
                    # the left edge of this piece
                    corner_count += 1
                    direction = 0

        # now, see if this piece has any interior regions and if so, include
        # those as well
        for region in self.get_interior_regions(coords):
            corner_count += self.count_sides(region)

        # print(f"Corner Count: {corner_count}")
        return corner_count

    def get_interior_regions(self, coords):
        # find any holes inside of coords, and return them as separate regions
        # coords is a list of (x, y) tuples
        interior_regions = []
        visited = set(coords)

        # Check bounds, assuming coordinates are non-negative
        # print(f"Checking interior regions for: {coords}")
        min_x = min(x for x, y in coords)
        max_x = max(x for x, y in coords)
        min_y = min(y for x, y in coords)
        max_y = max(y for x, y in coords)

        # print(f"Interior Region Check: min_x={min_x}, max_x={max_x}, min_y={min_y}, max_y={max_y}")

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) not in visited:
                    # print(f"Starting flood fill at: ({x}, {y})")
                    # Start flood fill from an unvisited inside point
                    touches_wall, interior_region = False, []
                    stack = [(x, y)]
                    while stack:
                        cx, cy = stack.pop()
                        if (cx, cy) in visited:
                            continue
                        if cx < min_x or cx > max_x or cy < min_y or cy > max_y:
                            touches_wall = True
                            continue
                        visited.add((cx, cy))
                        interior_region.append((cx, cy))
                        # print(f"Visited: ({cx}, {cy})")

                        # Explore the four directions
                        stack.extend([(cx + dx, cy + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

                    if touches_wall:
                        interior_region = []

                    if interior_region:
                        # print(f"Found interior region: {interior_region}")
                        interior_regions.append(interior_region)

        # print(f"Total interior regions found: {len(interior_regions)}")
        return interior_regions

    def solve_part_two(self):
        price = 0
        self.visited = set()
        for coordinate in self.coordinates:
            if coordinate not in self.visited:
                # print(f"Processing coordinate: {coordinate}")
                coordinates, region_size, _ = self.flood_fill(coordinate)
                sides_count = self.count_sides(coordinates)
                # print(f"Flood fill found region size {region_size} with {sides_count} sides")
                price += region_size * sides_count
        # print(f"Total price calculated in Part Two: {price}")
        return price
