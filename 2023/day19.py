import click
import sys

from collections import defaultdict

VERBOSE = False


class Rule:
    def __init__(self, id, rules):
        self.id = id
        self.default = rules[-1]
        self.flat = False
        self.rules = []
        for rule in rules[0:-1]:
            if rule in ("A", "R"):
                self.rules.append(rule)
            elif ":" in rule:
                cond, tgt = rule.split(":", 1)
                self.rules.append([cond[0], cond[1], int(cond[2:]), tgt])

    def __repr__(self):
        return "Rule[%s]: %s or %s" % (self.id, self.rules, self.default)

    def flatten(self, rules):
        if self.flat:
            return
        self.flat = True

        if self.default not in ("A", "R"):
            self.default = rules[self.default]
            self.default.flatten(rules)

        for idx in range(len(self.rules)):
            if type(self.rules[idx]) == str:
                if self.rules[idx] not in ("A", "R"):
                    self.rules[idx] = rules[self.rules[idx]]
                    self.rules[idx].flatten(rules)
            else:
                if self.rules[idx][3] not in ("A", "R"):
                    self.rules[idx][3] = rules[self.rules[idx][3]]
                    self.rules[idx][3].flatten(rules)

    def classify(self, part):
        log(part)

        ruler = self
        while True:
            # log(ruler)
            trip = False
            for rule in ruler.rules:
                # log(rule)
                if type(rule) == str:
                    # str means it's A or R guaranteed
                    return rule
                if rule[1] == "<":
                    if part[rule[0]] < rule[2]:
                        trip = True
                elif rule[1] == ">":
                    if part[rule[0]] > rule[2]:
                        trip = True
                else:
                    raise Exception("fuck2")
                if not trip:
                    continue
                if type(rule[3]) == str:
                    return rule[3]
                else:
                    ruler = rule[3]
                    break
            if not trip:
                if type(ruler.default) == str:
                    return ruler.default
                ruler = ruler.default

    def constrain(self, xmas):
        # counter
        ct = 0

        def count(xmast):
            ct2 = (
                ((xmast["x"][1] - xmast["x"][0]) + 1)
                * ((xmast["m"][1] - xmast["m"][0]) + 1)
                * ((xmast["a"][1] - xmast["a"][0]) + 1)
                * ((xmast["s"][1] - xmast["s"][0]) + 1)
            )
            # log("Rcount>>", ct2, xmas)
            return ct2

        def accept(xmast):
            log(
                "Accepted:",
                [[xmast[char][0], xmast[char][1]] for char in ("x", "m", "a", "s")],
            )
            return count(xmast)

        # basically assume x/m/a/s are tuples of min/max and execute
        # rules until we get to 'accepts'
        for rule in self.rules:
            # if we get the final rule and it accepts, we can return the count based on
            # the permutations here
            log()
            log(">>RULE", rule)
            log(xmas)

            # save sanity later
            char, cond, val, tgt = rule

            # if this is an accept rule, apply and then either recurse or continue
            if type(tgt) == str:
                if tgt == "A":
                    # rules that immediately accept mean we have to count up the delta
                    # that would "now be accepted" and increment by that, then constrain
                    # to continue rule processing
                    # delta = 0

                    tmp = {k: xmas[k].copy() for k in xmas.keys()}
                    if cond == ">" and val < xmas[char][1]:
                        # delta = xmas[char][1] - max(xmas[char][0], val)
                        tmp[char][0] = val + 1
                        xmas[char][1] = val
                    elif cond == "<" and val > xmas[char][0]:
                        # delta = min(xmas[char][1], val) - xmas[char][0]
                        tmp[char][1] = val - 1
                        xmas[char][0] = val
                    ct += accept(tmp)

                    # accepts have to add count! there's probably a better way
                    # muls = [delta]
                    # for charz in xmas.keys():
                    #    if char == charz:
                    #        continue
                    #    muls.append(xmas[charz][1] - xmas[charz][0])

                    # count increase
                    # ct += (muls[0] + 1) * (muls[1] + 1) * (muls[2] + 1) * (muls[3] + 1)

                elif tgt == "R":
                    # rejects apply the limits inversely! but then we don't need to do
                    # anything else
                    if cond == ">":
                        xmas[char][1] = min(xmas[char][1], val)
                    elif cond == "<":
                        xmas[char][0] = max(xmas[char][0], val)

                # continue rule processing, on to the next rule
                continue

            # we're going into a rule, but only for some delta of matches,
            # which means we need to raise the OTHER side of the limit to pass
            # down to the children before we continue on with our own
            xmas2 = {k: xmas[k].copy() for k in xmas.keys()}
            if cond == ">" and val < xmas2[char][1]:
                xmas[char][1] = val
                xmas2[char][0] = val + 1
            elif cond == "<" and val > xmas2[char][0] and val <= xmas2[char][1]:
                xmas[char][0] = val
                xmas2[char][1] = val - 1

            # get count from child with a copy of our xmas list
            ct += tgt.constrain(xmas2)

        # now we're down to default
        if type(self.default) == str:
            if self.default == "A":
                return accept(xmas) + ct
            elif self.default == "R":
                return ct
        else:
            return self.default.constrain(xmas) + ct


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
    p1 = True
    rules = {}
    parts = []

    for line in inp:
        if p1:
            if not line:
                p1 = False
                continue
            name, rule = line.split("{", 1)
            rules[name] = Rule(name, rule[0:-1].split(","))
        else:
            part = {}
            for prt in line[1:-1].split(","):
                idx, val = prt.split("=", 1)
                part[idx] = int(val)
            parts.append(part)

    rule = rules["in"]
    rule.flatten(rules)

    return rule, parts


def part1(inp):
    rule, parts = inp

    rv = 0
    for part in parts:
        if rule.classify(part) == "A":
            rv += sum(part.values())
    return rv


def part2(inp):
    rule, parts = inp

    v = rule.constrain({"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]})
    ev = 167409079868000
    log(v, ev, v - ev)
    return v


if __name__ == "__main__":
    main()
