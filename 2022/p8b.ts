import * as fs from "fs";
import { arrayBuffer } from "stream/consumers";

// y, x, height
var trees: Array<Array<number>> = new Array();
var scores: Array<Array<number>> = new Array();

fs.readFileSync("inputs/day8.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    trees.push(new Array(...line.split("").map((elem) => parseInt(elem))));
    scores.push(new Array(trees[trees.length - 1].length).fill(0));
  });

// Hope it's a square
const MAX_X = trees[0].length - 1;
const MAX_Y = trees.length - 1;

// Calculate score for each tree
for (var y = 0; y <= MAX_Y; y++) {
  for (var x = 0; x <= MAX_X; x++) {
    var treeHeight = trees[y][x];

    // Calculate rightwards view
    var rightScore = 0;
    if (x < MAX_X) {
      for (var mx = x + 1; mx <= MAX_X; mx++) {
        rightScore++;
        if (trees[y][mx] >= treeHeight) {
          break;
        }
      }
    }

    // Calculate leftwards
    var leftScore = 0;
    if (x > 0) {
      for (var mx = x - 1; mx >= 0; mx--) {
        leftScore++;
        if (trees[y][mx] >= treeHeight) {
          break;
        }
      }
    }

    // Calculate downwards view
    var downScore = 0;
    if (y < MAX_Y) {
      for (var my = y + 1; my <= MAX_Y; my++) {
        downScore++;
        if (trees[my][x] >= treeHeight) {
          break;
        }
      }
    }

    // Calculate upwards
    var upScore = 0;
    if (y > 0) {
      for (var my = y - 1; my >= 0; my--) {
        upScore++;
        if (trees[my][x] >= treeHeight) {
          break;
        }
      }
    }

    // Fill in scenic score
    // console.log(y, x, leftScore, rightScore, upScore, downScore);
    scores[y][x] = leftScore * rightScore * upScore * downScore;
  }
}

console.log(Math.max(...scores.map((arry) => Math.max(...arry))));
