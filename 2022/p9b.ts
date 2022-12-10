import { assert } from "console";
import * as fs from "fs";

class Point {
  x: number = 0;
  y: number = 0;

  move(dir: string) {
    switch (dir) {
      case "U":
        this.y--;
        break;
      case "R":
        this.x++;
        break;
      case "L":
        this.x--;
        break;
      case "D":
        this.y++;
        break;
    }
  }

  follow(knot: Point) {
    // If the head is touching the tail, do nothing
    if (Math.abs(knot.x - this.x) <= 1 && Math.abs(knot.y - this.y) <= 1) {
      return;
    }

    // If the this is two steps in a column/row, move closer
    if (knot.x == this.x) {
      if (knot.y < this.y) {
        this.y--;
      } else {
        this.y++;
      }
    } else if (knot.y == this.y) {
      if (knot.x < this.x) {
        this.x--;
      } else {
        this.x++;
      }
    } else {
      // Diagonal, move whichever way takes us closer
      if (knot.x < this.x && knot.y < this.y) {
        this.x--;
        this.y--;
      } else if (knot.x < this.x && knot.y > this.y) {
        this.x--;
        this.y++;
      } else if (knot.x > this.x && knot.y < this.y) {
        this.x++;
        this.y--;
      } else if (knot.x > this.x && knot.y > this.y) {
        this.x++;
        this.y++;
      } else {
        assert("shitty stuff happened");
      }
    }
  }
}

var knots: Array<Point> = new Array();
var visited: Record<string, boolean> = {};

for (var i = 0; i < 10; i++) {
  knots.push(new Point());
}

function visit(loc: Point) {
  visited[loc.x + ":" + loc.y] = true;
}

visit(knots[knots.length - 1]);

fs.readFileSync("inputs/day9.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    var [dir, steps] = line.split(/ /, 2);

    for (var ctr = 0; ctr < parseInt(steps); ctr++) {
      knots[0].move(dir);
      for (var idx = 1; idx < knots.length; idx++) {
        knots[idx].follow(knots[idx - 1]);
      }
      visit(knots[knots.length - 1]);
    }
    return;
  });

console.log(visited);
console.log(Object.keys(visited).length);
