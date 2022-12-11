import { assert } from "console";
import * as fs from "fs";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day11." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

console.log(options.P1 ? part1(lines) : part2(lines));

// DRAGONS HERE

function part1(lines: Array<string>): number {
  lines.forEach((line) => {
    if (!line) return;

    //
    console.log(line);
  });
  return 0;
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  lines.forEach((line) => {
    if (!line) return;

    //
  });
  return 1;
}
