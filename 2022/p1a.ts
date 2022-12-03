import * as fs from "fs";

var elves: Array<number> = [0];

fs.readFileSync("inputs/day1.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (line == "") {
      elves.push(0);
    } else {
      elves[elves.length - 1] += parseInt(line);
    }
  });

console.log(
  elves.sort((a, b) => {
    return b - a;
  })[0]
);
