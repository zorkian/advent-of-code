import { assert } from "console";
import * as fs from "fs";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample").option("-debug");
program.parse();

const options = program.opts();
const filename = "inputs/day18." + (options.Sample ? "sample" : "input");

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
  z: number = 0;

  constructor(x: number, y: number, z: number) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
}

class Whatever {
  cubes: Map<string, number> = new Map();

  min: Point = new Point(999, 999, 999);
  max: Point = new Point(0, 0, 0);

  setCube(x: number, y: number, z: number) {
    this.cubes.set(x + ":" + y + ":" + z, 1);

    // Track the edges so we can 'flood' the map later
    this.min.x = Math.min(this.min.x, x - 1);
    this.min.y = Math.min(this.min.y, y - 1);
    this.min.z = Math.min(this.min.z, z - 1);
    this.max.x = Math.max(this.max.x, x + 1);
    this.max.y = Math.max(this.max.y, y + 1);
    this.max.z = Math.max(this.max.z, z + 1);
  }

  getCube(x: number, y: number, z: number): number {
    var key = x + ":" + y + ":" + z;
    if (this.cubes.has(key)) {
      return this.cubes.get(key)!;
    }
    return 0;
  }

  keyToCoords(key: string): [number, number, number] {
    var [x, y, z] = key.split(/:/).map((int) => parseInt(int));
    return [x, y, z];
  }

  adjacents(x: number, y: number, z: number): Array<[number, number, number]> {
    return [
      [x - 1, y, z],
      [x + 1, y, z],
      [x, y - 1, z],
      [x, y + 1, z],
      [x, y, z - 1],
      [x, y, z + 1],
    ];
  }

  part1(): number {
    var score = 0;
    dbg(this.cubes);
    [...this.cubes.keys()].forEach((cube) => {
      var [x, y, z] = this.keyToCoords(cube);
      this.adjacents(x, y, z).forEach((test) => {
        dbg(">", test);
        score += this.getCube(test[0], test[1], test[2]) ? 0 : 1;
      });
    });
    return score;
  }

  part2(): number {
    var score = 0;
    var next: Array<Point> = [new Point(this.min.x, this.min.y, this.min.z)];
    var visited: Map<string, boolean> = new Map();

    while (next.length > 0) {
      // Pop something off the list, if we can see walls here then we know we
      // can score them... if there's nothing, add it to our BFS flooding
      var cur = next.pop()!;

      this.adjacents(cur.x, cur.y, cur.z).forEach((cube) => {
        if (
          cube[0] < this.min.x ||
          cube[0] > this.max.x ||
          cube[1] < this.min.y ||
          cube[1] > this.max.y ||
          cube[2] < this.min.z ||
          cube[2] > this.max.z
        ) {
          return;
        }

        var type = this.getCube(cube[0], cube[1], cube[2]);
        var key = cube[0] + ":" + cube[1] + ":" + cube[2];
        if (type == 0) {
          if (visited.has(key)) {
            return;
          }
          next.push(new Point(cube[0], cube[1], cube[2]));
          visited.set(key, true);
        } else if (type == 1) {
          // Safe to increment, nobody else can count this face
          score++;
        } else {
          throw "programmer error, don't feed";
        }
      });
    }
    return score;
  }
}

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();
  lines.forEach((line) => {
    if (!line) return;

    var [x, y, z] = line.split(/,/).map((int) => parseInt(int));
    res.setCube(x, y, z);
  });

  return res;
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);

  return input.part1();
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  return input.part2();
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
