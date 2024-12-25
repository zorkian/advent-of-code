from .day import Day


class Day23(Day):
    def __init__(self, use_test_data=False):
        self.connections = {}
        super().__init__(day_number=23, use_test_data=use_test_data)

    def parse_input(self):
        for line in self.input_data:
            computer_a, computer_b = line.split("-")
            if computer_a not in self.connections:
                self.connections[computer_a] = set()
            if computer_b not in self.connections:
                self.connections[computer_b] = set()
            self.connections[computer_a].add(computer_b)
            self.connections[computer_b].add(computer_a)

    def solve_part_one(self):
        interconnected_sets = set()
        for computer in self.connections:
            if not computer.startswith("t"):
                continue
            neighbors = self.connections[computer]
            for neighbor in neighbors:
                for second_neighbor in neighbors:
                    if (
                        second_neighbor != neighbor
                        and second_neighbor in self.connections[neighbor]
                    ):
                        interconnected_set = {computer, neighbor, second_neighbor}
                        if len(interconnected_set) == 3:
                            interconnected_sets.add(frozenset(interconnected_set))
        return len(interconnected_sets)

    def find_fully_interconnected_sets(self):
        def is_fully_interconnected(computers):
            for comp in computers:
                if not all(
                    other in self.connections[comp]
                    for other in computers
                    if other != comp
                ):
                    return False
            return True

        intercon_sets = []
        visited = set()

        for computer in self.connections:
            if computer not in visited:
                current_set = {computer}
                visited.add(computer)

                # Find all interconnected computers
                for other in self.connections[computer]:
                    if other not in visited and is_fully_interconnected(
                        current_set | {other}
                    ):
                        current_set.add(other)
                        visited.add(other)

                if (
                    len(current_set) > 1
                ):  # Only consider sets with more than one computer
                    intercon_sets.append(current_set)

        return intercon_sets

    def solve_part_two(self):
        intercon_sets = self.find_fully_interconnected_sets()

        largest_set = max(intercon_sets, key=len)

        result = ",".join(sorted(largest_set))
        print("Answer:", result)
        return len(largest_set)
