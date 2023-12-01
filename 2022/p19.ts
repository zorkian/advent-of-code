import { assert } from "console";
import * as fs from "fs";
import { debugPort } from "process";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample").option("-debug");
program.parse();

const options = program.opts();
const filename = "inputs/day19." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n/);

const DEBUG = options.Debug;
function dbg(...args: any) {
  if (DEBUG) {
    console.log(...args);
  }
}

// PARSING LIZARDS HERE

class Robot {
  type: string = "";
  ore_cost: number = 0;
  clay_cost: number = 0;
  obsidian_cost: number = 0;
}

class Blueprint {
  id: number = 0;

  ore_bot: Robot = new Robot();
  clay_bot: Robot = new Robot();
  obsidian_bot: Robot = new Robot();
  geode_bot: Robot = new Robot();

  max_ore(): number {
    return Math.max(
      this.ore_bot.ore_cost,
      this.clay_bot.ore_cost,
      this.obsidian_bot.ore_cost,
      this.geode_bot.ore_cost
    );
  }

  max_clay(): number {
    return this.obsidian_bot.clay_cost;
  }

  max_obsidian(): number {
    return this.geode_bot.obsidian_cost;
  }

  part1_rev(target: number) {
    // Given a target number, see if we can hit it ... this is a reverse
    // calculation to try to limit the search space (since there are so
    // many _wrong_ ways to do this...)
    // Calculate how many geode-minutes we'll need and then break that up
    // into the different patterns that we could use to achieve those
  }

  part1(
    time: number,
    robots: Map<string, number>,
    ores: Map<string, number>
  ): number {
    // Given time minutes left, with current stockpile of X, attempt to maximize
    // the score by choosing from all of the available options
    if (time <= 0) {
      dbg("returning", ores.get("geode")!);
      return ores.get("geode")!;
    }
    // dbg(time, robots, ores);

    // First, generate ores
    robots.forEach((count, ore) => {
      ores.set(ore, ores.get(ore)! + count);
    });

    // Now, let's find all possible actions we can take and put them into the
    // list and then DFS it...
    var funcs = new Array();

    // Construct an ore robot possibility; or wait for ore to build it
    if (robots.get("ore")! < this.max_ore()) {
      if (ores.get("ore")! >= this.ore_bot.ore_cost) {
        funcs.push((): number => {
          var lrobots = new Map(robots);
          var lores = new Map(ores);
          // dbg("building ore bot");
          lrobots.set("ore", lrobots.get("ore")! + 1);
          lores.set("ore", lores.get("ore")! - this.ore_bot.ore_cost);
          return this.part1(time - 1, lrobots, lores);
        });
      }
    }

    // Construct a clay robot possibility
    if (robots.get("clay")! < this.max_clay()) {
      if (ores.get("ore")! >= this.clay_bot.ore_cost) {
        funcs.push((): number => {
          var lrobots = new Map(robots);
          var lores = new Map(ores);
          // dbg("building clay bot");
          lrobots.set("clay", lrobots.get("clay")! + 1);
          lores.set("ore", lores.get("ore")! - this.clay_bot.ore_cost);
          return this.part1(time - 1, lrobots, lores);
        });
      }
    }

    // Construct an obisidian robot possibility
    if (robots.get("obsidian")! < this.max_obsidian()) {
      if (
        ores.get("ore")! >= this.obsidian_bot.ore_cost &&
        ores.get("clay")! >= this.obsidian_bot.clay_cost
      ) {
        funcs.push((): number => {
          var lrobots = new Map(robots);
          var lores = new Map(ores);
          // dbg("building obsidian bot");
          lrobots.set("obsidian", lrobots.get("obsidian")! + 1);
          lores.set("ore", lores.get("ore")! - this.obsidian_bot.ore_cost);
          lores.set("clay", lores.get("clay")! - this.obsidian_bot.clay_cost);
          return this.part1(time - 1, lrobots, lores);
        });
      }
    }

    // Construct a geode bot possibility
    if (
      ores.get("ore")! >= this.geode_bot.ore_cost &&
      ores.get("obsidian")! >= this.geode_bot.obsidian_cost
    ) {
      funcs.push((): number => {
        var lrobots = new Map(robots);
        var lores = new Map(ores);
        // dbg("building geode bot");
        lrobots.set("geode", lrobots.get("geode")! + 1);
        lores.set("ore", lores.get("ore")! - this.geode_bot.ore_cost);
        lores.set(
          "obsidian",
          lores.get("obsidian")! - this.geode_bot.obsidian_cost
        );
        return this.part1(time - 1, lrobots, lores);
      });
    }

    // We can always wait a turn... this helps us to construct bots
    // we might not otherwise do (by waiting)
    funcs.push((): number => {
      return this.part1(time - 1, new Map(robots), new Map(ores));
    });

    // Let's try each of the actions, and return the best score
    var score: number = 0;
    funcs.forEach((func) => {
      score = Math.max(score, func());
    });
    return score;
  }
}

class Whatever {
  blueprints: Map<number, Blueprint> = new Map();

  part1(
    time: number,
    robots: Map<string, number>,
    ores: Map<string, number>
  ): number {
    var scores: Array<[number, number]> = new Array();
    this.blueprints.forEach((bp, id) => {
      scores.push([id, bp.part1(time, new Map(robots), new Map(ores), 0)]);
    });
    scores.sort((a, b) => b[1] - a[1]);
    dbg(scores);
    return scores[0][0] * scores[0][1];
  }
}

function parse(lines: Array<string>): Whatever {
  var res = new Whatever();

  lines.forEach((line) => {
    if (!line) return;

    // Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    var m = line.match(/^Blueprint (\d+): (.+)$/)!;

    var bpt = new Blueprint();
    bpt.id = parseInt(m[1]);

    m[2].split(/\./).forEach((bp) => {
      if (!bp) return;

      m = bp.match(
        /Each (.+) robot costs (\d+) ore(?: and (\d+) (clay|obsidian))?/
      )!;

      var rb = new Robot();
      rb.type = m[1];
      rb.ore_cost = parseInt(m[2]);
      if (m[4] == "clay") {
        rb.clay_cost = parseInt(m[3]);
      } else if (m[4] == "obsidian") {
        rb.obsidian_cost = parseInt(m[3]);
      } else if (m[4]) {
        throw "mog doa':w";
      }

      if (rb.type == "ore") {
        bpt.ore_bot = rb;
      } else if (rb.type == "clay") {
        bpt.clay_bot = rb;
      } else if (rb.type == "obsidian") {
        bpt.obsidian_bot = rb;
      } else if (rb.type == "geode") {
        bpt.geode_bot = rb;
      } else {
        throw "god no why";
      }
    });

    res.blueprints.set(bpt.id, bpt);
  });

  return res;
}

// DRAGONS HERE

function part1(lines: Array<string>): number {
  var input = parse(lines);

  // Initialize with a single ore robot
  var robots: Map<string, number> = new Map();
  robots.set("ore", 1);
  robots.set("clay", 0);
  robots.set("obsidian", 0);
  robots.set("geode", 0);

  // Initialize with no ores
  var ores: Map<string, number> = new Map();
  ores.set("ore", 0);
  ores.set("clay", 0);
  ores.set("obsidian", 0);
  ores.set("geode", 0);

  // Now let's send out our factory
  return input.part1(24, robots, ores);
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  return 1;
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
