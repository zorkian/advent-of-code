import { assert } from "console";
import * as fs from "fs";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample").option("-debug");
program.parse();

const options = program.opts();
const filename = "inputs/day17." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

const DEBUG = options.Debug;
function dbg(...args: any) {
  if (DEBUG) {
    console.log(...args);
  }
}

// PARSING LIZARDS HERE

class Point {
  x: number = 0;
  y: number = 0;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

const shapes = [
  // Horizontal line
  [new Point(0, 0), new Point(1, 0), new Point(2, 0), new Point(3, 0)],

  // Plus
  [
    new Point(1, 0),
    new Point(0, 1),
    new Point(1, 1),
    new Point(2, 1),
    new Point(1, 2),
  ],

  // Right L
  [
    new Point(0, 0),
    new Point(1, 0),
    new Point(2, 0),
    new Point(2, 1),
    new Point(2, 2),
  ],

  // Vertical line
  [new Point(0, 0), new Point(0, 1), new Point(0, 2), new Point(0, 3)],

  // Square
  [new Point(0, 0), new Point(1, 0), new Point(0, 1), new Point(1, 1)],
];

class Whatever {
  tiles: Array<number> = new Array(7).fill(0);

  moves: Array<number> = new Array();
  movect: number = 0;

  bounds(piece: Array<Point>): [Point, Point] {
    var min = new Point(999, 999);
    var max = new Point(0, 0);

    piece.forEach((point) => {
      min.x = Math.min(min.x, point.x);
      min.y = Math.min(min.y, point.y);
      max.x = Math.max(max.x, point.x);
      max.y = Math.max(max.y, point.y);
    });

    return [min, max];
  }

  highest(): number {
    return Math.max(...this.tiles);
  }

  nextMove(): number {
    return this.moves[this.movect++ % this.moves.length];
  }
}

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();
  lines.forEach((line) => {
    if (!line) return;

    line.split("").forEach((char) => {
      if (char == "<") {
        res.moves.push(-1);
      } else {
        res.moves.push(1);
      }
    });
  });

  return res;
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);

  var idx = 0;
  for (var i = 0; i < 2022; i++) {
    var piece = shapes[idx++ % shapes.length];
    var [min, max] = input.bounds(piece);

    var offset_x = 2;
    var offset_y = input.highest() + 4;

    var stopped = false;
    while (!stopped) {
      // Shift left/right if possible
      var move = input.nextMove();
      if (min.x + offset_x + move < 0 || max.x + offset_x + move >= 7) {
        dbg("can't offset through walls", move);
      } else {
        // Determine if we're going to bang into another piece
        var canMove = true;
        piece.every((point) => {
          if (input.tiles[point.x + offset_x + move] >= point.y + offset_y) {
            dbg("can't offset through piece", move);
            canMove = false;
            return false;
          }
          return true;
        });
        if (canMove) {
          dbg("offsetting", move);
          offset_x += move;
        }
      }

      // Now determine if we will collide
      var canDrop = true;
      piece.every((point) => {
        var test = new Point(point.x + offset_x, point.y + offset_y);
        if (input.tiles[test.x] >= test.y - 1) {
          canDrop = false;
          return false;
        }
        return true;
      });
      if (canDrop) {
        dbg("dropping");
        offset_y--;
      } else {
        piece.forEach((point) => {
          input.tiles[point.x + offset_x] = Math.max(
            input.tiles[point.x + offset_x],
            point.y + offset_y
          );
        });
        dbg("landed", input.tiles);
        stopped = true;
      }
    }
  }

  return input.highest();
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  return 1;
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
