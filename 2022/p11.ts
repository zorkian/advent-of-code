import { assert } from "console";
import * as fs from "fs";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day11." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

// DRAGONS HERE

enum Operator {
  add = 0,
  multiply,
}

class Operation {
  operator: Operator = Operator.add;
  right: number | undefined = 0; // undefined to use left side

  apply(item: number) {
    const t_right = this.right == undefined ? item : this.right;
    if (this.operator == Operator.add) {
      return item + t_right;
    } else if (this.operator == Operator.multiply) {
      return item * t_right;
    } else {
      throw "unknown operator";
    }
  }
}

class Monkey {
  id: number = 0;
  items: Array<number> = new Array();
  inspections: number = 0;
  operation: Operation = new Operation();
  test_divisible_by: number = 0;
  if_true_monkey: number = 0;
  if_false_monkey: number = 0;

  is_turn_over(): boolean {
    return this.items.length == 0 ? true : false;
  }

  inspect_and_throw_to_part1(): Array<number> {
    this.inspections++;
    var item = Math.floor(this.operation.apply(this.items.shift()!) / 3);
    if (item % this.test_divisible_by == 0) {
      return [this.if_true_monkey, item];
    } else {
      return [this.if_false_monkey, item];
    }
  }

  inspect_and_throw_to_part2(mb: number): Array<number> {
    this.inspections++;
    var item = this.operation.apply(this.items.shift()!) % mb;
    if (item % this.test_divisible_by == 0) {
      return [this.if_true_monkey, item];
    } else {
      return [this.if_false_monkey, item];
    }
  }
}

function part1(lines: Array<string>): number {
  var monkeys: Array<Monkey> = new Array();

  var monkey: Monkey;

  lines.forEach((line) => {
    if (!line) return;

    var res;
    if ((res = line.match(/Monkey (\d+)/))) {
      monkey = new Monkey();
      monkey.id = parseInt(res[1]);
      if (monkey.id != monkeys.length) {
        throw "out of order monkey";
      }
      monkeys.push(monkey);
    } else if ((res = line.match(/Starting items: (.+)/))) {
      monkey.items = res[1].split(/, /).map((elem) => parseInt(elem));
    } else if ((res = line.match(/Operation: new = old (.+?) (.+)/))) {
      monkey.operation = new Operation();
      if (res[1] == "*") {
        monkey.operation.operator = Operator.multiply;
      } else if (res[1] == "+") {
        monkey.operation.operator = Operator.add;
      } else {
        throw "invalid operation";
      }
      if (res[2] == "old") {
        monkey.operation.right = undefined;
      } else {
        monkey.operation.right = parseInt(res[2]);
      }
    } else if ((res = line.match(/Test: divisible by (.+)/))) {
      monkey.test_divisible_by = parseInt(res[1]);
    } else if ((res = line.match(/If true: throw to monkey (.+)/))) {
      monkey.if_true_monkey = parseInt(res[1]);
    } else if ((res = line.match(/If false: throw to monkey (.+)/))) {
      monkey.if_false_monkey = parseInt(res[1]);
    } else {
      throw "invalid monkey";
    }
  });

  for (var ctr = 0; ctr < 20; ctr++) {
    for (var i = 0; i < monkeys.length; i++) {
      while (!monkeys[i].is_turn_over()) {
        const [throw_to, item] = monkeys[i].inspect_and_throw_to_part1();
        monkeys[throw_to].items.push(item);
      }
    }
  }

  var top_monkeys = monkeys
    .map((monkey) => [monkey.inspections, monkey.id])
    .sort((a, b) => b[0] - a[0]);

  return top_monkeys[0][0] * top_monkeys[1][0];
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var monkeys: Array<Monkey> = new Array();

  var monkey: Monkey;

  lines.forEach((line) => {
    if (!line) return;

    var res;
    if ((res = line.match(/Monkey (\d+)/))) {
      monkey = new Monkey();
      monkey.id = parseInt(res[1]);
      if (monkey.id != monkeys.length) {
        throw "out of order monkey";
      }
      monkeys.push(monkey);
    } else if ((res = line.match(/Starting items: (.+)/))) {
      monkey.items = res[1].split(/, /).map((elem) => parseInt(elem));
    } else if ((res = line.match(/Operation: new = old (.+?) (.+)/))) {
      monkey.operation = new Operation();
      if (res[1] == "*") {
        monkey.operation.operator = Operator.multiply;
      } else if (res[1] == "+") {
        monkey.operation.operator = Operator.add;
      } else {
        throw "invalid operation";
      }
      if (res[2] == "old") {
        monkey.operation.right = undefined;
      } else {
        monkey.operation.right = parseInt(res[2]);
      }
    } else if ((res = line.match(/Test: divisible by (.+)/))) {
      monkey.test_divisible_by = parseInt(res[1]);
    } else if ((res = line.match(/If true: throw to monkey (.+)/))) {
      monkey.if_true_monkey = parseInt(res[1]);
    } else if ((res = line.match(/If false: throw to monkey (.+)/))) {
      monkey.if_false_monkey = parseInt(res[1]);
    } else {
      throw "invalid monkey";
    }
  });

  var mb: number = monkeys.reduce(
    (accum, monkey) => accum * monkey.test_divisible_by,
    1
  );

  for (var ctr = 0; ctr < 10000; ctr++) {
    for (var i = 0; i < monkeys.length; i++) {
      while (!monkeys[i].is_turn_over()) {
        const [throw_to, item] = monkeys[i].inspect_and_throw_to_part2(mb);
        monkeys[throw_to].items.push(item);
      }
    }
  }

  var top_monkeys = monkeys
    .map((monkey) => [monkey.inspections, monkey.id])
    .sort((a, b) => b[0] - a[0]);

  return top_monkeys[0][0] * top_monkeys[1][0];
}

// CLOSING

console.log(options.P1 ? part1(lines) : part2(lines));
