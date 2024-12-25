from .day import Day

import itertools


class Day24(Day):
    def __init__(self, use_test_data=False):
        self.wire_values = {}
        self.operations = {}
        self.registers = {}
        self.swaps = {}
        super().__init__(day_number=24, use_test_data=use_test_data)

    def parse_input(self):
        for swap in [('z18', 'hmt'), ('bfq', 'z27'), ('hkh', 'z31'), ('bng', 'fjp')]:
            self.swaps[swap[0]] = swap[1]
            self.swaps[swap[1]] = swap[0]

        for line in self.input_data:
            if not line:
                continue
            if ": " in line:
                key, value = line.split(": ")
                key = key.strip()
                self.wire_values[key] = value.strip()
            else:
                parts = line.split()
                outreg = self.fr(parts[4])
                self.operations[outreg] = parts[:-2]

                reg1 = parts[0]
                reg2 = parts[2]

                if (
                    (reg1.startswith("x") and reg2.startswith("y"))
                    or (reg1.startswith("y") and reg2.startswith("x"))
                ) and reg1[1:3] == reg2[1:3]:
                    bit = int(reg1[1:3])
                    if bit not in self.registers:
                        self.registers[bit] = {}
                    if parts[1] == "AND":
                        self.registers[bit]["carry"] = outreg
                        self.registers[outreg] = "carry"
                    elif parts[1] == "XOR":
                        self.registers[bit]["sum"] = outreg
                        self.registers[outreg] = "sum"
        print(self.registers)

    def prepare_string(self, routput):
        # change where we're outputting if we're screwing with it
        output = self.swaps.get(routput, routput)

        # the fun calculations begin now
        if output in self.wire_values:
            return (self.wire_values[output], set())
        if output not in self.operations:
            raise ValueError(f"Output {output} not found in operations")

        gates = {self.operations[output][0], self.operations[output][2]}

        o1, g1 = self.prepare_string(self.operations[output][0])
        gates = gates.union(g1)

        o2, g2 = self.prepare_string(self.operations[output][2])
        gates = gates.union(g2)

        return (
            "("
            + o1
            + {
                "AND": "&",
                "OR": "|",
                "XOR": "^",
            }[self.operations[output][1]]
            + o2
            + ")",
            gates,
        )

    def solve_part_one(self):
        rv = 0
        for i in range(46, -1, -1):
            out = f"z{i:02}"
            if out not in self.operations:
                continue
            prep, _ = self.prepare_string(out)
            evald = eval(prep)
            # print(out, '=', prep, evald)
            rv += evald << i
        return rv

    def fr(self, reg):
        return self.swaps.get(reg, reg)

    def validate_bit(self, bit, carry_in=None):
        # if bit is 45, we're done
        if bit == 45:
            return True

        # try to validate
        carry, sum = self.registers[bit]["carry"], self.registers[bit]["sum"]

        # if this is bit 0, sum should be z00, then recurse with our carry for
        # the next bits
        if bit == 0:
            if sum != "z00":
                print(f"bit {bit} sum {sum} != z00")
                return False
            return self.validate_bit(1, carry)

        # find two operations where carry_in/sum are the participants, those are
        # the next part of the adder
        next_carry, next_sum = None, None
        for op in self.operations:
            lop, rop = self.operations[op][0], self.operations[op][2]
            if (
                (lop == carry_in and rop == sum) or (lop == sum and rop == carry_in)
            ) and (self.operations[op][1] == "AND"):
                if next_carry:
                    print(f"bit {bit} multiple carry operations")
                    return False
                next_carry = op
            if (
                (lop == carry_in and rop == sum) or (lop == sum and rop == carry_in)
            ) and (self.operations[op][1] == "XOR"):
                if next_sum:
                    print(f"bit {bit} multiple sum operations")
                    return False
                next_sum = op
        print(
            f"bit {bit}: carry_in {carry_in}, carry {carry}, sum {sum}, next_carry {next_carry}, next_sum {next_sum}"
        )

        if not next_carry or not next_sum:
            print(f"bit {bit} missing carry or sum operation {next_carry} {next_sum}")
            return False

        # the sum goes out to the output register
        if next_sum != f"z{bit:02}":
            print(f"bit {bit} next_sum {next_sum} != z{bit:02}")
            return False

        # carry and next_carry should have an operation of AND somewhere, find it
        carry_out = None
        for op in self.operations:
            lop, rop = self.operations[op][0], self.operations[op][2]
            if (
                (lop == carry and rop == next_carry)
                or (lop == next_carry and rop == carry)
            ) and (self.operations[op][1] == "OR"):
                if carry_out:
                    print(f"bit {bit} multiple carry_out operations")
                    return False
                carry_out = op

        print(
            f"bit {bit}: carry {carry}, sum {sum}, next_carry {next_carry}, next_sum {next_sum}, carry_out {carry_out}"
        )

        # we have everything now, move to next bit
        return self.validate_bit(bit + 1, carry_out)

    def solve_part_two(self):
        xvalue = 123123123123123
        yvalue = 123123123123123
        zvalue = 246246246246246
        zvals = {}
        for i in range(50):
            self.wire_values[f"x{i:02}"] = str((xvalue >> i) & 1)
            self.wire_values[f"y{i:02}"] = str((yvalue >> i) & 1)
            zvals[f"z{i:02}"] = (zvalue >> i) & 1
        # print all x and y values
        # for i in range(50):
        #    print(f"x{i:02} = {self.wire_values[f'x{i:02}']}")
        #    print(f"y{i:02} = {self.wire_values[f'y{i:02}']}")
        # print(zvals)

        self.validate_bit(0)

        return 0
