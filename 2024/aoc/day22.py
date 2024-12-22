from .day import Day


class Day22(Day):
    def __init__(self, use_test_data=False):
        super().__init__(day_number=22, use_test_data=use_test_data)

    def parse_input(self):
        self.numbers = []
        for line in self.input_data:
            self.numbers.append(int(line))

    def mix(self, secret, number):
        return (secret ^ number)

    def prune(self, number):
        return number % 16777216

    def next_secret(self, number):
        a = self.prune(self.mix(number, number * 64))
        b = self.prune(self.mix(a, a // 32))
        c = self.prune(self.mix(b, b * 2048))
        return c

    def solve_part_one(self):
        rv = 0
        for num in self.numbers:
            for _ in range(2000):
                num = self.next_secret(num)
            rv += num
        return rv

    def solve_part_two(self):
        seqs = {}
        totals = {}
        setseqs = set()

        for num in self.numbers:
            onum = num
            seqs[onum] = {}
            lastfour = []
            for _ in range(2000):
                tnum = self.next_secret(num)
                price = tnum % 10

                lastfour.append(price - (num % 10))
                if len(lastfour) > 4:
                    lastfour = lastfour[1:]

                    # store the highest price this sequence has seen
                    # WRONG. store the FIRST.
                    lf = tuple(lastfour)
                    if lf not in seqs[onum]:
                        seqs[onum][lf] = price
                    setseqs.add(lf)

                #print(tnum, lastfour)
                num = tnum

            for seq in seqs[onum]:
                totals[seq] = totals.get(seq, 0) + seqs[onum][seq]

        # try to make the highest score
        #tmp = {}
        #for seq in setseqs:
        #    tmp[seq] = sum([seqs[num].get(seq, 0) for num in seqs.keys()])

        #for num in self.numbers:
        #    print(num, seqs[num].get((0, 0, -2, 2), None))

        #import pprint
        #pprint.pprint(totals)

        highest_seq = max(totals, key=totals.get)
        highest_value = totals[highest_seq]
        # print(f"Highest sequence: {highest_seq}, Total: {highest_value}")

        #highest_seq = max(tmp, key=tmp.get)
        #highest_value = tmp[highest_seq]
        #print(f"Highest sequence: {highest_seq}, Value: {highest_value}")

        return highest_value
