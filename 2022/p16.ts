import { assert } from "console";
import * as fs from "fs";
import { inflate } from "zlib";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day16." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

const DEBUG = true;
function dbg(...args: any) {
  if (DEBUG) {
    console.log(...args);
  }
}

// PARSING LIZARDS HERE

class Room {
  name: string = "";
  pressure: number = 0;
  doors: Array<string> = new Array();
  rooms: Map<string, Room> = new Map();

  constructor(name: string, pressure: number, doors: Array<string>) {
    this.name = name;
    this.pressure = pressure;
    this.doors = doors;
  }

  value(timeLeft: number, steps: number): number {
    // dbg("value:", this.name, timeLeft, steps);
    return (timeLeft - steps - 1) * this.pressure;
  }
}

class DoorScores {
  doors: Array<[string, number, number]> = new Array();
  sorted: boolean = false;
  idx: number = 0;

  reset() {
    this.idx = 0;
  }

  sort() {
    this.doors.sort((a, b) => b[1] - a[1]);
    this.sorted = true;
  }

  pop(): [string?, number?, number?] {
    if (!this.sorted) {
      this.sort();
    }
    if (this.idx >= this.doors.length) {
      return [undefined, undefined, undefined];
    }
    return this.doors[this.idx++];
  }

  hasMore(): boolean {
    return this.idx < this.doors.length;
  }

  push(door: string, time: number, score: number) {
    this.sorted = false;
    this.doors.push([door, time, score]);
  }

  copy(): DoorScores {
    return new DoorScores(this.doors);
  }

  constructor(doors: Array<[string, number, number]>) {
    this.doors = new Array(...doors);
  }
}

class Actor {
  room: Room;
  until: number;

  constructor(where: Room, until: number) {
    this.room = where;
    this.until = until;
  }
}

class Whatever {
  doors: Array<string> = new Array();
  rooms: Map<string, Room> = new Map();
  choices: Map<number, Map<string, DoorScores>> = new Map();

  part1(cur: Room, time: number, previsited: Array<string>): number {
    if (time <= 0) {
      return 0;
    }
    // dbg("part1:", cur.name, time, previsited);

    // Start by previsiting
    previsited.push(cur.name);

    // CHICKEN START

    // Score moves if we turn on each of the remaining valves from
    // the position we're at now
    var values: Map<string, [number, number]> = new Map();
    var visited: Set<string> = new Set([cur.name]);
    var next: Array<[number, string]> = new Array();
    var doors: Array<string> = new Array();

    // Initialize with our current room's exits
    // Now BFS any doors from here that haven't been visited yet
    cur.doors.forEach((door) => {
      next.push([1, door]);
    });

    // Walk and do a BFS
    while (next.length > 0) {
      // dbg(next);
      var [steps, room] = next.shift()!;

      // If unreachable (out of time), exit
      if (time - steps - 1 <= 0) {
        continue;
      }
      // dbg("evaluating", steps, room);

      // Get room we're visiting, visit it
      cur = this.rooms.get(room)!;
      visited.add(cur.name);
      if (previsited.indexOf(cur.name) >= 0) {
        // This has already been turned on so it has no score
        values.set(cur.name, [0, 0]);
      } else {
        // Consider this
        doors.push(cur.name);
        values.set(cur.name, [time - steps - 1, cur.value(time, steps)]);
      }

      // Now BFS any doors from here that haven't been visited yet
      cur.doors.forEach((door) => {
        // dbg("evaluate", door);
        if (!visited.has(door)) {
          next.push([steps + 1, door]);
          // dbg("pushed", door);
        }
      });
    }
    // dbg("DONE EVAL", values);

    // Now select the room to visit based on the maximum score
    // that we saw and the calculated timeLeft if we go to that room
    doors.sort((a, b) => values.get(b)![1] - values.get(a)![1]);

    // Now let's try each of them and find the best resulting score
    var scores: Map<string, number> = new Map();
    doors.forEach((door) => {
      // No sense continuing once we hit the zero scores
      var [timeLeft, score] = values.get(door)!;
      // dbg("go to:", previsited.join(" "), door, score);
      if (score == 0) {
        scores.set(door, score);
        return;
      }

      // Attempt to travel from this point
      scores.set(
        door,
        score + this.part1(this.rooms.get(door)!, timeLeft, previsited)
      );
    });

    // CHICKEN

    // Score moves if we turn on each of the remaining valves from
    // the position we're at now
    var values2: DoorScores = this.ranked_rooms(time, cur);

    // Now let's try each of them and find the best resulting score
    var scores2: Map<string, number> = new Map();
    while (values2.hasMore()) {
      var [door, timeAfter, score] = values2.pop();

      // dbg("go to:", previsited.join(" "), door, score);
      if (score == 0) {
        scores2.set(door!, score);
      } else {
        // Attempt to travel from this point
        scores2.set(
          door!,
          score! + this.part1(this.rooms.get(door!)!, timeAfter!, previsited)
        );
      }
    }
    dbg("scores=", values, "scores2=", values2);

    // We're done previsiting now
    previsited.pop();

    // Base case: nobody scored, return 0
    // var doors: Array<string> = [...scores2.keys()];
    if (doors.length == 0) {
      // dbg("return 0");
      return 0;
    }

    // Sort the doors by the final scores
    doors.sort((a, b) => scores.get(b)! - scores.get(a)!);
    // dbg(doors, scores);

    return scores.get(doors[0])!;
  }

  // Get ranked choices from a room, given an amount of time left
  ranked_rooms(time: number, orig: Room): DoorScores {
    // Memoization check
    if (this.choices.has(time)) {
      var tmp = this.choices.get(time)!;
      if (tmp.has(orig.name)) {
        return tmp.get(orig.name)!.copy();
      }
    } else {
      this.choices.set(time, new Map());
    }

    // Score moves if we turn on each of the remaining valves from
    // the position we're at now
    var cur: Room = orig;
    var scores: DoorScores = new DoorScores([]);
    var visited: Set<string> = new Set([cur.name]);
    var next: Array<[number, string]> = new Array();

    // Initialize with our current room's exits
    orig.doors.forEach((door) => {
      next.push([1, door]);
    });

    // Walk and do a BFS, calculating the value for each of the rooms
    // that we come across based on how far it is from the original
    // room that we started walking from
    while (next.length > 0) {
      // dbg(next);
      var [steps, room] = next.shift()!;

      // If unreachable (out of time), don't continue down this path
      // as there's nothing beyond here that can be closer
      if (time - steps - 1 <= 0) {
        continue;
      }

      // Get room we're visiting, visit it, add score to doorscores
      cur = this.rooms.get(room)!;
      visited.add(cur.name);
      scores.push(cur.name, time - steps - 1, cur.value(time, steps));

      // Now BFS any doors from here that haven't been visited yet
      cur.doors.forEach((door) => {
        if (!visited.has(door)) {
          next.push([steps + 1, door]);
        }
      });
    }

    // Memoize
    this.choices.get(time)!.set(orig.name, scores);
    return scores.copy();
  }

  // Time based function that takes in (time left, actor1, actor2)
  // Memoize the walkable choices from each location, and do a post-memo
  //     filtration pass (i.e., don't worry about memoizing the rooms that
  //     you already visited, it's ok if they show up)
  part2(
    orig: Room,
    cur: Room,
    time: number,
    previsited: Array<string>,
    me: boolean
  ): number {
    if (time < 2) {
      // Exit case OR elephant time
      if (me) {
        // Time to spin up the elephant and send it stampeding into the void
        // from the place that we started, never visiting anything we've already
        // visited
        return this.part2(orig, orig, 26, new Array(...previsited), false);
      }
      return 0;
    }
    // dbg("part2:", cur.name, time, previsited, me);

    // Start by previsiting
    previsited.push(cur.name);

    // Score moves if we turn on each of the remaining valves from
    // the position we're at now
    var values: DoorScores = this.ranked_rooms(time, cur);

    // Now let's try each of them and find the best resulting score
    var scores: Map<string, number> = new Map();
    while (values.hasMore()) {
      var [door, timeAfter, score] = values.pop();

      // dbg("go to:", previsited.join(" "), door, score);
      if (score == 0) {
        scores.set(door!, score);
      } else {
        // Attempt to travel from this point
        scores.set(
          door!,
          score! +
            this.part2(orig, this.rooms.get(door!)!, timeAfter!, previsited, me)
        );
      }
    }

    // We're done previsiting now
    previsited.pop();

    // Base case: nobody scored, return 0
    var doors: Array<string> = [...scores.keys()];
    if (doors.length == 0) {
      // dbg("return 0");
      if (me) {
        return this.part2(orig, orig, 26, new Array(...previsited), false);
      }
      return 0;
    }

    // Sort the doors by the final scores
    doors.sort((a, b) => scores.get(b)! - scores.get(a)!);
    dbg(doors, scores);

    return scores.get(doors[0])!;
  }

  inflate() {
    this.rooms.forEach((room) => {
      this.doors.push(room.name);
      room.doors.forEach((door) => {
        room.rooms.set(door, this.rooms.get(door)!);
      });
    });
  }
}

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();

  lines.forEach((line) => {
    if (!line) return;

    var m = line.match(
      /Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)/
    );
    if (!m) {
      throw "nope";
    }
    var room = new Room(m[1], parseInt(m[2]), m[3].split(/, /));
    res.rooms.set(room.name, room);
  });

  res.inflate();
  return res;
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);

  return input.part1(input.rooms.get("AA")!, 30, new Array());
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  var start = input.rooms.get("AA")!;
  return input.part2(start, start, 26, new Array(), true);
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
