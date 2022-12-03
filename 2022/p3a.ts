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

fs.readFileSync("inputs/day3.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    var p1 = new Set(line.slice(0, line.length / 2).split(""));
    var p2 = new Set(line.slice(line.length / 2, line.length).split(""));

    var xtras = [...p2].filter((elem) => p1.has(elem));
    [...p1].filter((elem) => p2.has(elem)).forEach((elem) => xtras.push(elem));

    score += calculateScore(new Set(xtras));
  });

console.log(score);
