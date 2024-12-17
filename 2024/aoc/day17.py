from .day import Day
from enum import Enum


class Operator(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Day17(Day):
    def __init__(self, use_test_data=False):
        self.registers = {"A": 0, "B": 0, "C": 0}
        self.program = []
        self.instructions = []
        self.instruction_pointer = 0
        self.output = []
        super().__init__(day_number=17, use_test_data=use_test_data)

    def parse_input(self):
        self.registers["A"] = int(self.input_data[0].split(":")[1].strip())
        self.registers["B"] = int(self.input_data[1].split(":")[1].strip())
        self.registers["C"] = int(self.input_data[2].split(":")[1].strip())
        self.program = list(map(int, self.input_data[4].split(":")[1].split(",")))

        for i in range(0, len(self.program), 2):
            operator = Operator(self.program[i])
            operand = self.program[i + 1]
            self.instructions.append((operator, operand))

    def get_value_from_operand(self, combo):
        if 0 <= combo <= 3:
            return combo
        elif combo == 4:
            return self.registers["A"]
        elif combo == 5:
            return self.registers["B"]
        elif combo == 6:
            return self.registers["C"]
        elif combo == 7:
            assert False, "Invalid combo operand"
        else:
            raise ValueError("Combo operand out of range")

    def solve_part_one(self):
        self.execute_program()
        print("Part 1 result: " + ",".join([str(i) for i in self.output]))
        return 0

    def reset(self, a=0):
        self.output = []
        self.registers["A"] = a
        self.registers["B"] = 0
        self.registers["C"] = 0
        self.instruction_pointer = 0

    def solve_part_two(self):
        # byte offset to increment from, start incrementer, value we're trying
        plen = len(self.program)
        boff, inc, val = (plen - 1) * 3, 1, 0
        while True:
            val += inc << boff

            self.reset(a=val)
            self.execute_program()

            if len(self.output) != plen:
                continue
            if self.output == self.program:
                return val

            if False:
                bit_string = f"{val:048b}"
                spaced_bit_string = " ".join(
                    bit_string[i : i + 3] for i in range(0, len(bit_string), 3)
                )
                print(
                    f"{spaced_bit_string} ...output = {self.output} ({len(self.output)})"
                )

            miscompare = False
            for comp in range(((plen * 3) - boff) // 3):
                if self.output[(plen - 1) - comp] != self.program[(plen - 1) - comp]:
                    miscompare = True
            if miscompare:
                val -= inc << boff
                inc += 1
                continue

            # it compared, move to next three-bits
            inc = 0
            boff -= 3

        assert "you have failed"

    def execute_program(self, output_required=None):
        temp_ip = 0
        while temp_ip < len(self.instructions):
            operator, operand = self.instructions[temp_ip]
            method = getattr(self, operator.name)
            method(operand)
            if output_required is not None:
                if (
                    len(self.output)
                    and output_required[0 : len(self.output)] != self.output
                ):
                    return False
                elif self.output == output_required:
                    return True
            temp_ip = self.instruction_pointer // 2

    def ADV(self, operand):
        denominator = pow(2, self.get_value_from_operand(operand))
        self.registers["A"] = int(self.registers["A"] // denominator)
        self.instruction_pointer += 2
        return f"ADV: operand={operand}, new A={self.registers['A']}"

    def BXL(self, operand):
        self.registers["B"] ^= operand
        self.instruction_pointer += 2
        return f"BXL: operand={operand}, new B={self.registers['B']}"

    def BST(self, operand):
        self.registers["B"] = self.get_value_from_operand(operand) % 8
        self.instruction_pointer += 2
        return f"BST: new B={self.registers['B']}"

    def JNZ(self, operand):
        if self.registers["A"] != 0:
            self.instruction_pointer = operand
        else:
            self.instruction_pointer += 2
        return f"JNZ: A={self.registers['A']}, operand={operand}, new instruction pointer={self.instruction_pointer}"

    def BXC(self, operand):
        self.registers["B"] ^= self.registers["C"]
        self.instruction_pointer += 2
        return f"BXC: new B={self.registers['B']}"

    def OUT(self, operand):
        value = self.get_value_from_operand(operand) % 8
        self.output.append(value)
        self.instruction_pointer += 2
        return f"OUT: output={value}, current output={self.output}"

    def BDV(self, operand):
        denominator = pow(2, self.get_value_from_operand(operand))
        self.registers["B"] = int(self.registers["A"] // denominator)
        self.instruction_pointer += 2
        return f"BDV: operand={operand}, new B={self.registers['B']}"

    def CDV(self, operand):
        denominator = pow(2, self.get_value_from_operand(operand))
        self.registers["C"] = int(self.registers["A"] // denominator)
        self.instruction_pointer += 2
        return f"CDV: operand={operand}, new C={self.registers['C']}"
