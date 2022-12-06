import { assert } from "console";
import * as fs from "fs";

fs.readFileSync("inputs/day6.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    for (var i = 13; i < line.length; i++) {
      var testSet = new Set(line.substring(i - 13, i + 1));
      if (testSet.size == 14) {
        console.log(i + 1);
        return;
      }
    }
  });
