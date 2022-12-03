import * as fs from "fs";

var elves: Array<number> = [0];

function toChoiceScore(inp: string): number {
  return { X: 1, Y: 2, Z: 3 }[inp] || 0;
}

function toWinScore(t1: string, t2: string): number {
  return (
    {
      X: { A: 3, B: 0, C: 6 }[t1],
      Y: { A: 6, B: 3, C: 0 }[t1],
      Z: { A: 0, B: 6, C: 3 }[t1],
    }[t2] || 0
  );
}

function toNewChoice(t1: string, t2: string): string {
  return (
    {
      X: { A: "Z", B: "X", C: "Y" }[t1],
      Y: { A: "X", B: "Y", C: "Z" }[t1],
      Z: { A: "Y", B: "Z", C: "X" }[t1],
    }[t2] || "Z"
  );
}

let score: number = 0;
fs.readFileSync("inputs/day2.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;
    var [t1, t2] = line.split(/ +/);
    t2 = toNewChoice(t1, t2);
    score += toChoiceScore(t2) + toWinScore(t1, t2);
  });

console.log(score);
