import { assert } from "console";
import * as fs from "fs";

var stacks: Array<Array<string>> = [];
var state: number = 0;

function printStacks() {
  for (let ctr = 1; ctr <= stacks.length; ctr++) {
    console.log(ctr + ": " + stacks[ctr - 1].join(""));
  }
}

fs.readFileSync("inputs/day5.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    if (state == 0) {
      // reading initial stacks
      if (line.startsWith(" 1")) {
        // console.log(stacks);
        state = 1;
        return;
      }

      for (var ctr = 0; ctr < line.length / 4; ctr++) {
        if (stacks.length <= ctr) {
          stacks.push([]);
        }

        var elem = line.slice(ctr * 4, (ctr + 1) * 4);

        if (elem.startsWith("[")) {
          stacks[ctr].unshift(elem.slice(1, 2));
        }
      }

      // console.log("STACK:", line);
      return;
    }

    // reading and executing moves
    // console.log("MOVE:", line);

    const move = line.match(/move (\d+) from (\d+) to (\d+)/);
    const from = parseInt(move[2]);
    const to = parseInt(move[3]);

    for (let ctr = 0; ctr < parseInt(move[1]); ctr++) {
      if (stacks[from - 1].length <= 0) {
        console.log("Horrid things happened.");
        return;
      }
      stacks[to - 1].push(stacks[from - 1].pop()!);
    }

    // printStacks();
  });

var result: string = "";
stacks.forEach((elem) => {
  if (elem.length > 0) {
    result += elem.pop();
  }
});

console.log(result);
