import { assert } from "console";
import * as fs from "fs";

class Point {
  x: number = 0;
  y: number = 0;
}

var score: number = 0;
var head: Point = new Point();
var tail: Point = new Point();
var visited: Record<string, boolean> = {};

function visit(loc: Point) {
  visited[loc.x + ":" + loc.y] = true;
}

function moveHead(dir: string) {
  switch (dir) {
    case "U":
      head.y--;
      break;
    case "R":
      head.x++;
      break;
    case "L":
      head.x--;
      break;
    case "D":
      head.y++;
      break;
  }
}

function moveTail() {
  // If the head is touching the tail, do nothing
  if (Math.abs(head.x - tail.x) <= 1 && Math.abs(head.y - tail.y) <= 1) {
    return;
  }

  // If the tail is two steps in a column/row, move closer
  if (head.x == tail.x) {
    if (head.y < tail.y) {
      tail.y--;
    } else {
      tail.y++;
    }
  } else if (head.y == tail.y) {
    if (head.x < tail.x) {
      tail.x--;
    } else {
      tail.x++;
    }
  } else {
    // Diagonal, move whichever way takes us closer
    if (head.x < tail.x && head.y < tail.y) {
      tail.x--;
      tail.y--;
    } else if (head.x < tail.x && head.y > tail.y) {
      tail.x--;
      tail.y++;
    } else if (head.x > tail.x && head.y < tail.y) {
      tail.x++;
      tail.y--;
    } else if (head.x > tail.x && head.y > tail.y) {
      tail.x++;
      tail.y++;
    } else {
      assert("shitty stuff happened");
    }
  }
}

visit(tail);

fs.readFileSync("inputs/day9.sample", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    var [dir, steps] = line.split(/ /, 2);

    for (var ctr = 0; ctr < parseInt(steps); ctr++) {
      moveHead(dir);
      moveTail();
      visit(tail);
    }
  });

console.log(Object.keys(visited).length);
