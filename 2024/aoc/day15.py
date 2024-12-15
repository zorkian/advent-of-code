from sympy.assumptions.cnf import Ne
from .day import Day


class Day15(Day):
    def __init__(self, use_test_data=False):
        self.warehouse_map = {}
        self.warehouse_map2 = {}
        self.boxes = []
        self.boxes2 = []
        self.robot_position = None
        self.robot_position2 = None
        self.moves = []
        self.width = 0
        self.width2 = 0
        self.height = 0
        super().__init__(day_number=15, use_test_data=use_test_data)

    def parse_input(self):
        input_segments = "\n".join(self.input_data).strip().split("\n\n")
        warehouse_lines = input_segments[0].strip().split("\n")
        self.height = len(warehouse_lines)
        self.width = max(len(line) for line in warehouse_lines)
        self.width2 = self.width * 2

        for y, line in enumerate(warehouse_lines):
            for x, char in enumerate(line):
                if char == "@":
                    self.robot_position = (x, y)
                    self.robot_position2 = (x * 2, y)
                    self.warehouse_map2[(x * 2, y)] = "@"
                    self.warehouse_map2[(x * 2 + 1, y)] = "."
                elif char == "O":
                    self.boxes.append((x, y))
                    self.boxes2.append((x * 2, x * 2 + 1, y))
                    self.warehouse_map2[(x * 2, y)] = "["
                    self.warehouse_map2[(x * 2 + 1, y)] = "]"
                elif char == "#":
                    self.warehouse_map2[(x * 2, y)] = "#"
                    self.warehouse_map2[(x * 2 + 1, y)] = "#"
                elif char == ".":
                    self.warehouse_map2[(x * 2, y)] = "."
                    self.warehouse_map2[(x * 2 + 1, y)] = "."
                self.warehouse_map[(x, y)] = char

        if len(input_segments) > 1:
            move_string = ''.join(input_segments[1].strip().split('\n'))
            self.moves = list(move_string)

        #self.print_warehouse_map()

    def print_warehouse_map(self):
        for y in range(self.height):
            for x in range(self.width):
                if (
                    x == 0
                    or x == self.width - 1
                    or y == 0
                    or y == self.height - 1
                    or self.warehouse_map[(x, y)] == "#"
                ):
                    print("#", end="")  # Walls
                elif (x, y) == self.robot_position:
                    print("@", end="")  # Robot
                elif (x, y) in self.boxes:
                    print("O", end="")  # Boxes
                else:
                    print(".", end="")  # Empty space
            print()  # New line at the end of each row

    def print_warehouse_map2(self):
        for y in range(self.height):
            for x in range(self.width2):
                if self.warehouse_map2[(x, y)] == "#":
                    print("#", end="")  # Walls
                elif (x, y) == self.robot_position2:
                    print("@", end="")  # Robot
                elif (x, x + 1, y) in self.boxes2:
                    print("[", end="")  # Wide box
                elif (x - 1, x, y) in self.boxes2:
                    print("]", end="")  # Wide box end
                else:
                    print(".", end="")  # Empty space
            print()  # New line at the end of each row

    def process_move(self, move):
        directions = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
        if move not in directions:
            return

        dx, dy = directions[move]
        robot_x, robot_y = self.robot_position
        new_x = robot_x + dx
        new_y = robot_y + dy

        if (new_x, new_y) not in self.warehouse_map or self.warehouse_map[
            (new_x, new_y)
        ] == "#":
            return  # Wall, do not move

        if (new_x, new_y) in self.boxes:
            # Check if we can push boxes
            boxes_to_push = []
            push_x = new_x
            push_y = new_y

            # Collect all boxes in line with the robot's movement direction
            while (push_x, push_y) in self.boxes:
                boxes_to_push.append((push_x, push_y))
                push_x += dx
                push_y += dy

            next_x = push_x
            next_y = push_y

            if (next_x, next_y) in self.warehouse_map and self.warehouse_map[
                (next_x, next_y)
            ] != "#":
                # We can push the boxes
                for box in boxes_to_push:
                    # Move each box
                    self.boxes.remove(box)
                    self.boxes.append((box[0] + dx, box[1] + dy))
            else:
                return  # No space to push the boxes

        # Move robot
        self.robot_position = (new_x, new_y)

    def process_move2_leftright(self, move):
        directions = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
        if move not in directions:
            return

        dx, dy = directions[move]
        robot_x, robot_y = self.robot_position2
        new_x = robot_x + dx
        new_y = robot_y + dy

        if (new_x, new_y) not in self.warehouse_map2 or self.warehouse_map2[
            (new_x, new_y)
        ] == "#":
            return  # Wall, do not move

        box = self.any_box_present2(new_x, new_y)
        if (new_x, new_y) in self.warehouse_map2 and not box:
            # Move robot, this is an empty space (no box)
            self.robot_position2 = (new_x, new_y)
            return
        if box is None:
            raise Exception("nope")

        # Check if we can push boxes
        boxes_to_push = []
        push_x = box[0]
        push_y = new_y  # Won't change, we're left/right

        # Collect all boxes in line with the robot's movement direction
        while (push_x, push_x + 1, push_y) in self.boxes2:
            boxes_to_push.append((push_x, push_x + 1, push_y))
            push_x += dx * 2

        next_x = push_x if dx > 0 else push_x + 1
        next_y = push_y

        # We can't push boxes left/right any more this way, so make sure the next square
        # is a space so we can shift
        if (next_x, next_y) in self.warehouse_map2 and self.warehouse_map2[
            (next_x, next_y)
        ] != "#":
            # We can push the boxes
            for pbox in boxes_to_push:
                # Move each box one in the dy direction
                self.boxes2.remove(pbox)
                self.boxes2.append((pbox[0] + dx, pbox[1] + dx, pbox[2]))
        else:
            return  # No space to push the boxes

        # Move robot
        self.robot_position2 = (new_x, new_y)
        return True

    def any_box_present2(self, x, y):
        # Return the box if either edge of a wide box is in this square
        if (x - 1, x, y) in self.boxes2:
            return (x - 1, x, y)
        elif (x, x + 1, y) in self.boxes2:
            return (x, x + 1, y)
        return None

    def process_move2_updown(self, move):
        directions = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
        if move not in directions:
            return

        dx, dy = directions[move]
        robot_x, robot_y = self.robot_position2
        new_x = robot_x + dx
        new_y = robot_y + dy

        if (new_x, new_y) not in self.warehouse_map2 or self.warehouse_map2[
            (new_x, new_y)
        ] == "#":
            return  # Wall, do not move

        box = self.any_box_present2(new_x, new_y)
        if (new_x, new_y) in self.warehouse_map2 and box is None:
            # Move robot, this is an empty space (no box)
            self.robot_position2 = (new_x, new_y)
            return
        if box is None:
            raise Exception("nope")

        # Check if we can push boxes
        boxes_to_check, boxes_to_push = [box], []
        while boxes_to_check:
            box = boxes_to_check.pop(0)

            # If either of our spaces hits a wall, we have to abort
            if (
                (box[0], box[2] + dy) not in self.warehouse_map2
                or self.warehouse_map2[(box[0], box[2] + dy)] == "#"
                or (box[1], box[2] + dy) not in self.warehouse_map2
                or self.warehouse_map2[(box[1], box[2] + dy)] == "#"
            ):
                return

            if box not in boxes_to_push:
                boxes_to_push.append(box)

            b1 = self.any_box_present2(box[0], box[2] + dy)
            if b1 is not None:
                boxes_to_check.append(b1)
            b2 = self.any_box_present2(box[1], box[2] + dy)
            if b2 is not None and b2 != b1:
                boxes_to_check.append(b2)

        # No wall, every box goes up or down
        for pbox in boxes_to_push:
            # Move each box one in the dy direction
            self.boxes2.remove(pbox)
            self.boxes2.append((pbox[0], pbox[1], pbox[2] + dy))

        # Move robot
        self.robot_position2 = (new_x, new_y)
        return True

    def process_move2(self, move):
        if move in "<>":
            return self.process_move2_leftright(move)
        else:
            return self.process_move2_updown(move)

    def solve_part_one(self):
        for move in self.moves:
            self.process_move(move)
        # self.print_warehouse_map()
        return sum([100 * y + x for x, y in self.boxes])

    def solve_part_two(self):
        ct = 0
        for move in self.moves:
            #if ct % 100 == 0:
            #    print()
            #    print("Moving: ", move, ' Count:', ct)
            self.process_move2(move)
            #if ct % 100 == 0:
            #    self.print_warehouse_map2()
            ct += 1
        #self.print_warehouse_map2()
        return sum([100 * y + x for x, _, y in self.boxes2])
