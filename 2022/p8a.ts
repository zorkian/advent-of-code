import * as fs from "fs";
import { arrayBuffer } from "stream/consumers";

// y, x, height
var trees: Array<Array<number>> = new Array();
var seen: Array<Array<boolean>> = new Array();

var score: number = 0;

fs.readFileSync("inputs/day8.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    trees.push(new Array(...line.split("").map((elem) => parseInt(elem))));
    seen.push(new Array(trees[trees.length - 1].length));
  });

// Hope it's a square
const MAX_X = trees[0].length - 1;
const MAX_Y = trees.length - 1;

// Cast rays from the left
for (var y = 0; y <= MAX_Y; y++) {
  var maxHeight: number = trees[y][0];
  seen[y][0] = true;

  for (var x = 1; x <= MAX_X; x++) {
    if (trees[y][x] > maxHeight) {
      seen[y][x] = true;
      maxHeight = trees[y][x];
    }
  }
}

// Cast rays from the right
for (var y = 0; y <= MAX_Y; y++) {
  var maxHeight: number = trees[y][MAX_X];
  seen[y][MAX_X] = true;

  for (var x = MAX_X; x > 0; x--) {
    if (trees[y][x] > maxHeight) {
      seen[y][x] = true;
      maxHeight = trees[y][x];
    }
  }
}

// Cast rays from the top
for (var x = 0; x <= MAX_X; x++) {
  var maxHeight: number = trees[0][x];
  seen[0][x] = true;

  for (var y = 0; y <= MAX_Y; y++) {
    if (trees[y][x] > maxHeight) {
      seen[y][x] = true;
      maxHeight = trees[y][x];
    }
  }
}

// Cast rays from the top
for (var x = 0; x <= MAX_X; x++) {
  var maxHeight: number = trees[MAX_Y][x];
  seen[MAX_Y][x] = true;

  for (var y = MAX_Y; y > 0; y--) {
    if (trees[y][x] > maxHeight) {
      seen[y][x] = true;
      maxHeight = trees[y][x];
    }
  }
}

seen.forEach((arry) =>
  arry.forEach((elem) => {
    if (elem) score++;
  })
);

console.log(score);
