import click
import itertools
import math
import sys

from collections import defaultdict

VERBOSE = False
COUNT = 1000


class Type:
    FLIPFLOP = 0
    CONJUNCTION = 1
    BROADCASTER = 2
    DEBUG = 3


class Part:
    def __init__(self, line):
        name, dests = line.split(" -> ", 1)
        self.inputs = {}
        self.dests = dests.split(", ")
        self.counter = 0
        self.chains = {}
        if name.startswith("%"):
            self.type = Type.FLIPFLOP
            self.name = name[1:]
            self.ffstate = False
        elif name.startswith("&"):
            self.type = Type.CONJUNCTION
            self.name = name[1:]
            self.cmemory = {}
        elif name.startswith("!"):
            self.type = Type.DEBUG
            self.name = name[1:]
        elif name == "broadcaster":
            self.name = name
            self.type = Type.BROADCASTER

    def __repr__(self):
        return "Part[%s: %s -> %s]" % (self.name, self.type, self.dests)

    def conjunctionInit(self, parts):
        for part in parts:
            if self.name in part.dests:
                self.cmemory[part.name] = False
        log("CONJUNCTION INIT:", self.name, "has inputs", self.cmemory.keys())

    def isInitial(self):
        if self.type == Type.BROADCASTER:
            return True
        elif self.type == Type.FLIPFLOP:
            return self.ffstate == False
        elif self.type == Type.CONJUNCTION:
            return not any(self.cmemory.values())
        elif self.type == Type.DEBUG:
            return True
        raise Exception("fuck2")

    def isInitialRecursive(self):
        return (
            True
            if self.isInitial() and all([p.isInitialRecursive() for p in self.dests])
            else False
        )

    def sendToAll(self, pulse):
        rv = []
        for dest in self.dests:
            rv.append((dest, pulse, self.name))
        return rv

    def count(self):
        ct = self.counter
        self.counter = 0
        if ct > 0:
            log(self.name, "count is", ct)
        return ct

    def pulse(self, pulse, sender):
        if not pulse:
            self.counter += 1

        rv = []
        if self.type == Type.BROADCASTER:
            rv += self.sendToAll(pulse)
        elif self.type == Type.FLIPFLOP:
            if not pulse:
                self.ffstate = not self.ffstate
                rv += self.sendToAll(self.ffstate)
        elif self.type == Type.CONJUNCTION:
            if sender not in self.cmemory:
                raise Exception("fuck")
            self.cmemory[sender] = pulse
            if all(self.cmemory.values()):
                rv += self.sendToAll(False)
            else:
                rv += self.sendToAll(True)
        elif self.type == Type.DEBUG:
            pass
        # log("PULSE:", self.name, pulse, "from", sender, "output", rv)
        return rv

    def pulseMemoize(self, pulse, sender):
        # Our goal is to memoize if we END UP in the initial state,
        # not if we're STARTING there
        pass

    def replace(self, parts):
        d = []
        for dest in self.dests:
            if dest:
                d.append(parts[dest])
                parts[dest].inputs[self.name] = self
        self.dests = d

    def countChains2(self, sender, cycles):
        log("cc2:", self.name, sender, cycles)

        def hasAllInputs():
            return all(self.chains.get(input, None) for input in self.inputs.keys())

        if self.name == "broadcaster":
            self.chains["button"] = [1]
            log("BC", self.name, self.chains)
            for dest in self.dests:
                dest.countChains2(self.name, [1])
        elif self.type == Type.FLIPFLOP:
            self.chains[sender] = math.lcm(*[cycle * 2 for cycle in cycles])
            log("FF", self.name, self.chains, self.inputs.keys())
            for dest in self.dests:
                dest.countChains2(self.name, self.chains.values())
        elif self.type == Type.CONJUNCTION:
            self.chains[sender] = math.lcm(*cycles)
            log("CNJ", self.name, self.chains)
            if hasAllInputs():
                lcmul = math.lcm(*self.chains.values())
                for dest in self.dests:
                    dest.countChains2(self.name, [lcmul])

    def countChains(self, sofar):
        # base cases, the broadcaster emits 1 every time it gets pressed, which is
        # once per button cycle
        # log("countChains:", self.name)
        if self.type == Type.BROADCASTER:
            return [1]

        # see if we've already answered the question for all of our inputs and, if so,
        # return the union of them
        rv = []
        for input in self.inputs.keys():
            rv += self.chains.get(input, None) or [None]
        if all(rv):
            log("FILLED:", self.name, rv)
            return rv

        # if we're already in the set, return, we've already tried this run
        # and we can't do it yet
        if self.name in sofar:
            return None
        sofar.add(self.name)

        # now see how often our inputs are sending pulses our way
        self.chains = {
            input.name: input.countChains(sofar) for input in self.inputs.values()
        }
        log(self.name, self.inputs.keys(), self.chains)

        # if we're a flipflop, we just double all the input cycle lengths and
        # then we pulse on all those intervals
        if self.type == Type.FLIPFLOP:
            return self.countChains(sofar)
        elif self.type == Type.CONJUNCTION:
            # we only fire at the LCM of all of the input chains
            if not all(self.chains.values()):
                return None
            lcmul = None
            for val in self.chains.values():
                if lcmul is None:
                    lcmul = val
                else:
                    lcmul = lcm(lcmul, val)
            return [lcmul]

        # base case, we can't calculate this yet
        return None


def log(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


@click.command()
@click.option("-p1", is_flag=True, help="Run part 1.")
@click.option("-p2", is_flag=True, help="Run part 2.")
@click.option("-test", is_flag=True, help="Use test inputs.")
@click.option("-v", is_flag=True, help="Print verbosely.")
def main(p1, p2, test, v):
    global VERBOSE
    VERBOSE = v
    log("p1 =", p1, "|| p2 =", p2, "|| test =", test, "|| v =", v)
    inp = munge_input(load_input(test))
    log("Munged input:", inp, "\n")
    print(part1(inp) if p1 else part2(inp))


def load_input(test):
    prefix = "inputs/day" + sys.argv[0].split(".")[0][-2:] + "."
    with open(prefix + ("test" if test else "input")) as f:
        return [l.strip() for l in f.readlines()]


def munge_input(inp):
    """
    Convert the input lines into whatever structure we need to handle the
    problem of the day.
    """
    rv = []
    for line in inp:
        rv.append(Part(line))
    parts = {p.name: p for p in rv}
    for part in rv:
        if part.type == Type.CONJUNCTION:
            part.conjunctionInit(rv)
        for dest in part.dests:
            if dest not in parts:
                parts[dest] = Part("!" + dest + " -> ")
    return parts


def part1(inp):
    iters = []

    for cycle in range(COUNT):
        clow, chigh = 1, 0

        # do one button cycle, this runs until there are no more pulses
        # going through the system
        circ = inp["broadcaster"].pulse(False, "button")
        while circ:
            dest, pulse, sender = circ.pop(0)
            if pulse:
                chigh += 1
            else:
                clow += 1
            circ += inp[dest].pulse(pulse, sender)

        # now we can store this count
        iters.append((clow, chigh))

        # if we're in "initial" state, we're done and we have detected a
        # cycle and we can calculate now how many pulses we get
        if all([p.isInitial() for p in inp.values()]):
            log("Reached stable at", cycle + 1, "cycles.")
            break

    # calculate how many of each we get
    ctAll = int(COUNT / (cycle + 1))
    ctHead = COUNT - (ctAll * len(iters))
    assert ctHead >= 0, "fuck3"

    # add up
    clow, chigh = 0, 0
    for idx in range(len(iters)):
        clow += iters[idx][0] * ctAll
        chigh += iters[idx][1] * ctAll
    log(iters, cycle + 1, ctAll, ctHead)
    return clow * chigh


def part2(inp):
    # prune the inp to anything that doesn't ultimately filter down to rx
    # parts = set()

    # def pathToRX(part):
    #     if part.name in parts:
    #         return []
    #     parts.add(part.name)
    #     log(part)

    #     # base case, we are rx or we lead to rx
    #     if part.name == "rx" or "rx" in part.dests:
    #         return [part]

    #     # try each of our dests to see who does, return them
    #     rv = []
    #     for dest in part.dests:
    #         rv += pathToRX(inp[dest])
    #     if rv:
    #         rv = [part] + rv
    #     return rv

    # cnow, clast = 1, 0
    # while cnow > clast:
    #     log(cnow, clast)
    #     clast = cnow
    #     for part in inp.values():
    #         for dest in part.dests:
    #             if dest in parts:
    #                 parts.add(part.name)
    #     cnow = len(parts)

    # log(pathToRX(inp["broadcaster"]))

    # return 0

    for part in inp.values():
        part.replace(inp)
    bcast = inp["broadcaster"]

    log(bcast.countChains2("button", 1))
    # log(bcast.countChains2("button", 1))
    # log(bcast.countChains2("button", 1))
    return 0

    cycle = 0
    while True:
        cycle += 1
        if cycle % 1000 == 0:
            log("Cycle", cycle, "...")

        # do one button cycle, this runs until there are no more pulses
        # going through the system
        circ = inp["broadcaster"].pulse(False, "button")
        while circ:
            dest, pulse, sender = circ.pop(0)
            circ += inp[dest].pulse(pulse, sender)

        # see how many pulses rx got
        if inp["rx"].count() == 1:
            return cycle


if __name__ == "__main__":
    main()
