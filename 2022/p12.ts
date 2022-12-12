import { kStringMaxLength } from "buffer";
import { assert } from "console";
import * as fs from "fs";
import { pathToFileURL } from "url";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day12." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

// PARSING LIZARDS HERE

class Point {
  x: number = 0;
  y: number = 0;

  key(): string {
    return this.x + ":" + this.y;
  }

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

class Whatever {
  heights: Record<string, number> = {};
  max: Point = new Point(0, 0);
  start: Point = new Point(0, 0);
  end: Point = new Point(0, 0);

  setHeight(p: Point, height: string) {
    this.heights[p.key()] = height.charCodeAt(0) - "a".charCodeAt(0);

    if (p.x > this.max.x) {
      this.max.x = p.x;
    }
    if (p.y > this.max.y) {
      this.max.y = p.y;
    }
  }

  getHeight(p: Point): number {
    return this.heights[p.key()];
  }

  getSurrounding(p: Point): Array<Point> {
    var res = new Array();
    if (p.x > 0) {
      res.push(new Point(p.x - 1, p.y));
    }
    if (p.x < this.max.x) {
      res.push(new Point(p.x + 1, p.y));
    }
    if (p.y > 0) {
      res.push(new Point(p.x, p.y - 1));
    }
    if (p.y < this.max.y) {
      res.push(new Point(p.x, p.y + 1));
    }
    return res;
  }

  getValidSteps(p: Point): Array<Point> {
    return this.getSurrounding(p).filter(
      (pt) => this.getHeight(pt) <= this.getHeight(p) + 1
    );
  }

  treeize() {
    // Construct a tree of all valid paths that can be walked, where
    // the starting point is the root
  }
}

function pointFromKey(key: string) {
  var [x, y] = key.split(/:/, 2).map((val) => parseInt(val));
  return new Point(x, y);
}

function parse(lines: Array<string>): Whatever {
  var y: number = 0;
  var res: Whatever = new Whatever();

  lines.forEach((line) => {
    if (!line) return;

    var x: number = 0;
    line.split("").forEach((chr) => {
      if (chr == "S") {
        chr = "a";
        res.start.x = x;
        res.start.y = y;
      } else if (chr == "E") {
        chr = "z";
        res.end.x = x;
        res.end.y = y;
      }
      res.setHeight(new Point(x, y), chr);
      x++;
    });

    y++;
  });

  res.treeize();

  return res;
}

// DRAGONS HERE

function p1_h(pt: Point, input: Whatever): number {
  return Math.abs(pt.x - input.end.x) + Math.abs(pt.y - input.end.y);
}

function p1_astar(input: Whatever): number {
  var cur = new Point(input.start.x, input.start.y);

  var openSet: Set<String> = new Set([cur.key()]);
  var cameFrom: Record<string, string> = {};

  var gScore: Record<string, number> = {};
  gScore[cur.key()] = 0;

  function get_gScore(key: string): number {
    if (key in gScore) {
      return gScore[key];
    }
    return 1000000000;
  }

  var fScore: Record<string, number> = {};
  fScore[cur.key()] = p1_h(cur, input);

  while (openSet.size > 0) {
    // Find lowest fscore item
    var lowest = -1;
    [...openSet.keys()].forEach((key) => {
      var str = key as string;
      if (lowest == -1 || fScore[str] < lowest) {
        cur = pointFromKey(str);
        lowest = fScore[str];
      }
    });

    // If this is goal node, walk it back
    if (cur.x == input.end.x && cur.y == input.end.y) {
      var score = 0;
      var path = [cur];
      while (cur.x != input.start.x || cur.y != input.start.y) {
        cur = pointFromKey(cameFrom[cur.key()]);
        path.unshift(cur);
        score += 1;
      }
      // console.log(path);
      return score;
    }

    // A star meaty meat
    openSet.delete(cur.key());
    input.getValidSteps(cur).forEach((pt) => {
      var tentative_gScore = get_gScore(cur.key()) + 1;
      if (tentative_gScore < get_gScore(pt.key())) {
        cameFrom[pt.key()] = cur.key();
        gScore[pt.key()] = tentative_gScore;
        fScore[pt.key()] = tentative_gScore + p1_h(pt, input);
        openSet.add(pt.key());
      }
    });
  }

  return 99999999;
}

function p1_solveFrom(
  input: Whatever,
  cur: Point,
  visited: Record<string, boolean>,
  memos: Record<string, number | undefined>
): number | undefined {
  // Given a world state, a place we're at, and the nodes we've visited, try
  // to find the shortest path and return

  // If memo'd, return it
  if (cur.key() in memos) {
    return memos[cur.key()];
  }
  // console.log(cur, Object.keys(visited).length);

  // TODO: could reduce number of copies of visited out to here, instead of
  // doing it down in the map, if it matters
  visited[cur.key()] = true;

  // Iterate each valid, unvisited step
  var res = input
    .getValidSteps(cur)
    .filter((pt) => !(pt.key() in visited))
    .map((pt) => {
      // Base case: success is this way, 1 step, guaranteed to be the
      // shortest path so just return (but return 0 since we add 1 later)
      if (pt.x == input.end.x && pt.y == input.end.y) {
        return 0;
      }

      // Else, cascade into ourselves to find the shortest path
      return p1_solveFrom(input, pt, { ...visited }, memos);
    })
    .filter((val) => val != undefined);

  // If there was nothing valid here, bummer, dead end
  if (res.length == 0) {
    memos[cur.key()] = undefined;
    return undefined;
  }

  // Sort and return smallest, that's our shortest path
  var result = res.sort((a, b) => a! - b!)[0];
  memos[cur.key()] = result! + 1;
  return result! + 1;
}

function part1(lines: Array<string>): number {
  var input = parse(lines);

  return p1_astar(input);

  return p1_solveFrom(input, new Point(input.start.x, input.start.y), {}, {})!;

  // Where we're at currently
  var cur = new Point(input.start.x, input.start.y);
  var next = new Array();
  var visited: Record<string, boolean> = {};
  var steps = 0;

  // We've already visited home base
  visited[cur.key()] = true;

  // Breadth first search while we don't have it
  while (cur.x != input.end.x || cur.y != input.end.y) {
    // Get valid steps and filter by places we haven't visited
    input
      .getValidSteps(cur)
      .filter((pt) => !(pt.key() in visited))
      .forEach((pt) => {
        visited[pt.key()] = true;
        next.push(pt);
      });

    // Assume we're taking a step now
    steps++;

    // Pop the next location for cur
    cur = next.shift();
    console.log(steps, cur, input.end);
  }

  return steps;
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  // Get all the 'a' elevations
  var lowest = 999999;
  for (var tmp in input.heights) {
    if (input.heights[tmp] == 0) {
      var pt = pointFromKey(tmp);
      input.start.x = pt.x;
      input.start.y = pt.y;
      lowest = Math.min(lowest, p1_astar(input));
      // console.log("lowest = ", lowest);
    }
  }

  return lowest;
}

// DO IT ALL

console.log(options.P1 ? part1(lines) : part2(lines));
