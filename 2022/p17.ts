import { assert } from "console";
import * as fs from "fs";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day17." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

// PARSING LIZARDS HERE

const shapes = class Whatever {
  tiles: Array<number> = new Array(7).fill(0);
  moves: Array<number> = new Array();

  highest(): number {
    return Math.max(this.tiles);
  }
};

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();
  lines.forEach((line) => {
    if (!line) return;

    line.split("").forEach((char) => {
      if (char == "<") {
        res.moves.push(-1);
      } else {
        res.moves.push(1);
      }
    });
  });

  return new Whatever();
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);

  return 0;
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  return 1;
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
