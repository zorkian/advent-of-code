import * as fs from "fs";

let score: number = 0;

fs.readFileSync("inputs/day4.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    var [p1, p2] = line.split(/,/);

    var [p1a, p1b] = p1.split(/-/).map((elem) => parseInt(elem));
    var [p2a, p2b] = p2.split(/-/).map((elem) => parseInt(elem));

    if ((p1a >= p2a && p1b <= p2b) || (p2a >= p1a && p2b <= p1b)) {
      score++;
    }
  });

console.log(score);
