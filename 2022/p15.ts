import { assert } from "console";
import * as fs from "fs";
import { pathToFileURL } from "url";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day15." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

// PARSING LIZARDS HERE

class Point {
  x: number = 0;
  y: number = 0;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

const BEACON = 0;
const SENSOR = 1;

class Thing {
  loc: Point = new Point(0, 0);
  type: number = SENSOR;
  partner: Thing | undefined = undefined;

  constructor(loc: Point, type: number) {
    this.loc = loc;
    this.type = type;
  }

  distance(): number {
    return (
      Math.abs(this.loc.x - this.partner!.loc.x) +
      Math.abs(this.loc.y - this.partner!.loc.y)
    );
  }

  distanceto(pt: Point): number {
    return Math.abs(this.loc.x - pt.x) + Math.abs(this.loc.y - pt.y);
  }

  covered(pt: Point): boolean {
    // True if the pt CANNOT contain a beacon (because it's within our
    // Manhattan distance of our paired beacon)
    return this.distanceto(pt) <= this.distance();
  }

  line(y: number): Array<number> {
    var res = new Array();

    var delta_y = Math.abs(this.loc.y - y);
    var distance = this.distance();

    if (delta_y > distance) {
      // This line is not covered, return nothing basically
      res.push(-1, -1);
    } else {
      // This line is covered, subtract out the vertical distance
      distance -= delta_y;
      res.push(this.loc.x - distance, this.loc.x + distance);
    }

    return res;
  }
}

class Whatever {
  sensors: Array<Thing> = new Array();
  beacons: Array<Thing> = new Array();

  maxd: number = 0;
  minx: number = 0;
  maxx: number = 0;

  addPair(sensorloc: Point, beaconloc: Point) {
    var sensor = new Thing(sensorloc, SENSOR);
    sensor.partner = new Thing(beaconloc, BEACON);
    sensor.partner.partner = sensor; // ensure we can never free memory again
    this.sensors.push(sensor);
    this.beacons.push(sensor.partner);
    this.maxd = Math.max(this.maxd, sensor.distance() + 1);
    this.minx = Math.min(this.minx, sensor.loc.x);
    this.maxx = Math.max(this.maxx, sensor.loc.x);
  }
}

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();

  lines.forEach((line) => {
    if (!line) return;

    var m = line.match(
      /Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)/
    )!;

    var sensor = new Point(parseInt(m[1]), parseInt(m[2]));
    var beacon = new Point(parseInt(m[3]), parseInt(m[4]));
    res.addPair(sensor, beacon);
  });

  return res;
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);

  const y = 2000000;
  var score = 0;
  var str = "";
  for (var x = input.minx - input.maxd; x < input.maxx + input.maxd; x++) {
    var covered = false;
    input.sensors.every((sensor) => {
      if (sensor.covered(new Point(x, y))) {
        covered = true;
        input.beacons.every((beacon) => {
          if (beacon.loc.x == x && beacon.loc.y == y) {
            covered = false;
            return false;
          }
          return true;
        });
        return false;
      }
      return true;
    });
    if (covered) {
      score++;
      // str += "#";
    } else {
      // str += ".";
    }
  }
  // console.log(str);
  return score;
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  // This is kind of weird, but my thinking is that we start at (0,0) and we
  // iterate through every beacon that might chop up line 0 and we start
  // removing chunks from the line... this should reduce it to 4,000,000 line
  // chunks (100 operations?) which might be fast enough? might still take
  // a few minutes...
  for (var y = 0; y <= 4000000; y++) {
    var x = 0,
      lastx = 0;
    if (y % 1000 == 0) {
      // console.log("starting row", y);
    }
    while (x <= 4000000) {
      lastx = x;
      input.sensors.every((sensor) => {
        var line = sensor.line(y);
        if (x >= line[0] && x <= line[1]) {
          // console.log(y, x, "moves to", line[1] + 1);
          x = line[1] + 1;
        }
        return true;
      });
      if (x == lastx) {
        // We made it a whole loop without moving the x, so this
        // means we found our spot!
        return x * 4000000 + y;
      }
    }
  }
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
