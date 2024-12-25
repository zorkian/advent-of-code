from .day import Day


class Day25(Day):
    def __init__(self, use_test_data=False):
        self.locks = []
        self.keys = []
        super().__init__(day_number=25, use_test_data=use_test_data)

    def parse_input(self):
        current_block = []

        for line in self.input_data:
            if line.strip() == '':
                if current_block:
                    self.process_block(current_block)
                    current_block = []
            else:
                current_block.append(line)

        if current_block:
            self.process_block(current_block)

    def toval(self, inp, lock=False, key=False):
        val = {
            0: 0 if lock else 31,
            1: 1 if lock else 15,
            2: 3 if lock else 7,
            3: 7 if lock else 3,
            4: 15 if lock else 1,
            5: 31 if lock else 0,
        }[inp]
        return val

    def process_block(self, block):
        is_lock = block[0] == '#' * len(block[0])

        columns = len(block[0])
        column_counts = [0] * columns

        for line in block:
            for i in range(columns):
                if line[i] == '#':
                    column_counts[i] += 1

        for i in range(len(column_counts)):
            column_counts[i] -= 1

        if is_lock:
            #self.locks.append(sum([self.toval(column_counts[i], lock=True) << ((4-i) * 5) for i in range(len(column_counts))]))
            self.locks.append([5 - i for i in column_counts])
        else:
            self.keys.append(column_counts)
            #self.keys.append(sum([self.toval(column_counts[i], key=True) << ((4-i) * 5) for i in range(len(column_counts))]))
        #print()
        #print(self.locks)
        #print(self.keys)

    def solve_part_one(self):
        rv = 0
        for key in self.keys:
            for lock in self.locks:
                if all([key[i] <= lock[i] for i in range(5)]):
                    rv += 1
                #if key - lock == 0:
                #    rv += 1
        return rv

    def solve_part_two(self):
        return 0
