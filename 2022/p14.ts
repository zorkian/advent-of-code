import { assert } from "console";
import * as fs from "fs";
import { inflate } from "zlib";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day14." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

// PARSING LIZARDS HERE

const AIR = 0;
const WALL = 1;
const SAND = 2;

class Point {
  x: number = 0;
  y: number = 0;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

class Whatever {
  world: Record<number, Record<number, number>> = {};
  min: Point = new Point(999, 999);
  max: Point = new Point(0, 0);

  setPoint(point: Point, what: number) {
    if (this.world[point.y] == undefined) {
      this.world[point.y] = {};
    }
    this.world[point.y][point.x] = WALL;

    this.min.x = Math.min(this.min.x, point.x);
    this.min.y = Math.min(this.min.y, point.y);
    this.max.x = Math.max(this.max.x, point.x);
    this.max.y = Math.max(this.max.y, point.y);
  }

  getPoint(point: Point): number {
    if (point.y < this.min.y || point.y > this.max.y) {
      return AIR;
    }
    if (this.world[point.y][point.x] == undefined) {
      return AIR;
    }
    return this.world[point.y][point.x];
  }

  addLine(points: Array<Point>) {
    var curPoint: Point;
    points.forEach((point) => {
      if (curPoint == undefined) {
        curPoint = point;
      } else {
        if (curPoint.x == point.x) {
          var startY = Math.min(curPoint.y, point.y);
          var endY = Math.max(curPoint.y, point.y);
          for (var y = startY; y <= endY; y++) {
            this.setPoint(new Point(point.x, y), WALL);
          }
        } else if (curPoint.y == point.y) {
          var startX = Math.min(curPoint.x, point.x);
          var endX = Math.max(curPoint.x, point.x);
          for (var x = startX; x <= endX; x++) {
            this.setPoint(new Point(x, point.y), WALL);
          }
        } else {
          throw "non-flat line";
        }
        curPoint = point;
      }
    });
  }

  inflate_part1() {
    this.min.y = Math.min(this.min.y, 0);

    for (var y = this.min.y; y <= this.max.y; y++) {
      if (this.world[y] == undefined) {
        this.world[y] = {};
      }
    }
  }

  inflate_part2() {
    this.min.y = Math.min(this.min.y, 0);
    this.max.y += 2;

    for (var y = this.min.y; y <= this.max.y; y++) {
      if (this.world[y] == undefined) {
        this.world[y] = {};
      }
    }

    // Install "infinite" floor, hope this is big enough lul
    for (var x = this.min.x - 1000; x <= this.max.x + 1000; x++) {
      this.world[this.max.y][x] = WALL;
    }
  }

  simulateGrain(loc: Point): boolean {
    // Returns true if the grain landed in the grid, false if it went
    // out of bounds somewhere

    if (
      this.max.x < loc.x ||
      this.min.x > loc.x ||
      this.max.y < loc.y ||
      this.min.y > loc.y
    ) {
      throw "initial point not within bounds of lines";
    }

    // Simulate the grain
    while (true) {
      if (this.getPoint(loc) != AIR) {
        // This is the "sand backed up to the start" exit condition
        return false;
      }

      // Places the sand can go
      var locs = [
        new Point(loc.x, loc.y + 1),
        new Point(loc.x - 1, loc.y + 1),
        new Point(loc.x + 1, loc.y + 1),
      ];

      var nxt: Point | undefined = undefined;
      locs.every((pt) => {
        if (this.getPoint(pt) == AIR) {
          nxt = pt;
          return false;
        }
        return true;
      });

      if (nxt == undefined) {
        // We can't go anywhere, so we stay where we were, we're now FIXED
        // in PLACE and can return
        this.setPoint(loc, SAND);
        return true;
      }

      // Off the grid case
      if (loc.y < this.min.y || loc.y > this.max.y) {
        return false;
      }

      loc = nxt;
    }
  }
}

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();
  lines.forEach((line) => {
    if (!line) return;
    var points: Array<Point> = new Array();
    line.split(/ -> /).forEach((coords) => {
      var coordints = coords.split(/,/).map((coord) => parseInt(coord));
      points.push(new Point(coordints[0], coordints[1]));
    });
    res.addLine(points);
  });
  return res;
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);
  input.inflate_part1();
  console.log(input);

  var score: number = 0;
  while (input.simulateGrain(new Point(500, 0))) {
    // Generate a grain of sand at the point and then simulate it down
    // console.log("falling...", score);
    score++;
  }
  return score;
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);
  input.inflate_part2();

  var score: number = 0;
  while (input.simulateGrain(new Point(500, 0))) {
    // Generate a grain of sand at the point and then simulate it down
    // console.log("falling...", score);
    score++;
  }
  return score;
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
