import * as fs from "fs";

let score: number = 0;

function calculateScore(inp: Set<string>): number {
  var score = 0;

  inp.forEach((elem) => {
    let charScore = elem.charCodeAt(0);
    if (charScore >= 97) score += charScore - 96;
    else score += charScore - 64 + 26;
  });

  return score;
}

var tmp: Set<string>;
var ctr: number = 0;

fs.readFileSync("inputs/day3.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    ctr++;

    var p1 = new Set(line.split(""));

    if (ctr == 1) {
      tmp = p1;
      return;
    }

    tmp = new Set([...tmp].filter((elem) => p1.has(elem)));

    if (ctr == 3) {
      ctr = 0;
      score += calculateScore(tmp);
      tmp = new Set();
    }
  });

console.log(score);
