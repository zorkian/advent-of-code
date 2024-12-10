from .day import Day


class Day9(Day):
    def __init__(self, use_test_data=False, debug=False):
        self.debug = debug
        self.p1_output = [] # List of integers (-1 for free space, else it's a file ID) # List of integers (-1 for free space, else it's a file ID)
        self.p2_output = [] # List of tuples (-1 for free space or file ID, count of blocks) # List of tuples (-1 for free space or file ID, count of blocks)
        super().__init__(day_number=9, use_test_data=use_test_data)

    def parse_input(self):
        first_line = self.input_data[0].strip()
        sentinel = -1  # Define a sentinel value indicating free space
        self.p1_output = []

        for index, char in enumerate(first_line):
            count = int(char)
            # Add blocks of data or free space alternatively
            if index % 2 == 0:
                self.p1_output.extend([index // 2] * count)  # Add blocks of data
                self.p2_output.append((index // 2, count))
            else:
                self.p1_output.extend([sentinel] * count)  # Add blocks of free space
                self.p2_output.append((-1, count))

        if self.debug:
            print(self.p2_output)

        # self.compact_data()
        self.compact_p2()

        if self.debug:
            print(self.p2_output)
            print(self.calculate_checksum())
            print(self.calculate_checksum_p2())

    def calculate_checksum(self):
        checksum = sum(index * value for index, value in enumerate(self.p1_output) if value != -1)
        return checksum

    def calculate_checksum_p2(self):
        checksum, idx = 0, 0
        for i in range(len(self.p2_output)):
            if self.p2_output[i][0] != -1:
                checksum += sum([self.p2_output[i][0] * j for j in range(idx, idx + self.p2_output[i][1])])
            idx += self.p2_output[i][1]
        return checksum

    def compact_data(self):
        while True:
            last_valid_index = None
            moved = False

            for index in reversed(range(len(self.p1_output))):
                if self.p1_output[index] != -1:  # Found a data block
                    last_valid_index = index
                    break

            if last_valid_index is None:
                break  # Exit if there are no more blocks of data

            for index in range(len(self.p1_output)):
                if self.p1_output[index] == -1:  # Found free space
                    if last_valid_index is not None:
                        self.p1_output[index] = self.p1_output[last_valid_index]
                        self.p1_output[last_valid_index] = -1  # Mark the old position as free space
                        last_valid_index = None  # Reset last_valid_index to find the next data block
                        moved = True
                        break

            if moved:
                # Remove free space (-1's) on the right edge
                while self.p1_output and self.p1_output[-1] == -1:
                    self.p1_output.pop()
            else:
                break  # Exit if no moves were made in the last iteration

    def compact_p2(self):
        tried_ids = set()  # Keep track of moved file IDs
        moved = True

        while moved:
            moved = False
            for i in range(len(self.p2_output) - 1, 0, -1):
                if self.p2_output[i][0] != -1 and self.p2_output[i][0] not in tried_ids:  # Found a real data tuple we haven't moved yet
                    print(f"Trying {self.p2_output[i][0]}")
                    tried_ids.add(self.p2_output[i][0])
                    moved = True
                    data_count = self.p2_output[i][1]
                    if self.debug:
                        print(f"Checking data tuple {self.p2_output[i]} at index {i}")
                    for j in range(i):
                        if self.p2_output[j][0] == -1 and self.p2_output[j][1] >= data_count:
                            free_space_count = self.p2_output[j][1]
                            if self.debug:
                                print(f"Found free space at index {j} with count {free_space_count}")
                            if free_space_count > data_count:
                                # Split the free space range and swap only data_count blocks
                                self.p2_output[j] = (self.p2_output[i][0], data_count)
                                self.p2_output[i] = (-1, data_count)  # Adjust remaining free space count
                                # Insert a smaller free space block after the moved data
                                self.p2_output.insert(j + 1, (-1, free_space_count - data_count))
                                if self.debug:
                                    print(f"Moved data from index {i} to index {j}, updated p2_output: {self.p2_output}")
                            else:
                                # Move the data tuple to the free space
                                self.p2_output[j] = (self.p2_output[i][0], free_space_count)
                                self.p2_output[i] = (-1, self.p2_output[i][1])  # Mark old position as free space
                                if self.debug:
                                    print(f"Moved all data from index {i} to index {j}, updated p2_output: {self.p2_output}")
                            break

            # Compact free space by summing counts
            compacted_output = []
            current_free_space_count = 0
            for file_id, count in self.p2_output:
                if file_id == -1:  # it's free space
                    current_free_space_count += count
                else:
                    if current_free_space_count > 0:
                        compacted_output.append((-1, current_free_space_count))
                        current_free_space_count = 0
                    compacted_output.append((file_id, count))

            if current_free_space_count > 0:
                compacted_output.append((-1, current_free_space_count))

            self.p2_output = compacted_output
        print(self.p2_output)

    def solve_part_one(self):
        return self.calculate_checksum()

    def solve_part_two(self):
        return self.calculate_checksum_p2()
