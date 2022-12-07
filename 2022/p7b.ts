import { assert } from "console";
import * as fs from "fs";
import { nextTick } from "process";

class File {
  name: string;
  location?: Directory;
  size: number;

  constructor(name: string, size: number, location?: Directory) {
    this.name = name;
    this.size = size;
    this.location = location;
  }
}

class Directory extends File {
  contents: Record<string, File> = {};

  constructor(name: string, location?: Directory) {
    super(name, 0, location);
  }

  addFile(name: string, size: number) {
    this.size += size;
    this.contents[name] = new File(name, size, this);

    var nextc = this.location;
    while (nextc !== undefined) {
      nextc.size += size;
      nextc = nextc.location;
    }
  }

  addDirectory(name: string) {
    this.contents[name] = new Directory(name, this);
  }

  calculateScore(): number {
    var score = 0;
    for (const name in this.contents) {
      if (this.contents[name] instanceof Directory) {
        score += (this.contents[name] as Directory).calculateScore();
      }
    }

    if (this.size <= 100000) {
      score += this.size;
    }

    return score;
  }

  findClosestDirectorySize(target: number): number {
    // console.log(this.name, this.size, "looking for", target);

    var best = this.size;

    for (const name in this.contents) {
      if (!(this.contents[name] instanceof Directory)) {
        continue;
      }

      var dir = this.contents[name] as Directory;
      if (dir.size < target) {
        // console.log(dir.name, dir.size, "skipping");
        continue;
      }

      var testBest = dir.findClosestDirectorySize(target);
      if (testBest < best) {
        best = testBest;
      }
    }

    return best;
  }

  print(indent: number = 0) {
    console.log(" ".repeat(indent), this.name, this.size);
    for (const name in this.contents) {
      if (this.contents[name] instanceof Directory) {
        (this.contents[name] as Directory).print(indent + 2);
      }
    }
  }
}

var root = new Directory("/", undefined);
var cur = root;

fs.readFileSync("inputs/day7.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    if (line.startsWith("$")) {
      // Command to execute
      if (line.startsWith("$ ls")) {
        return;
      } else {
        var cd = line.split(/ /, 3)[2];
        if (cd == "..") {
          cur = cur.location!;
        } else if (cd == "/") {
          cur = root;
        } else if (cd in cur.contents) {
          cur = cur.contents[cd] as Directory;
        } else {
          assert("unknown");
        }
      }
    } else {
      // File/dir listing, add it to the current directory
      var [t1, t2] = line.split(/ /, 2);
      if (t1 == "dir") {
        cur.addDirectory(t2);
      } else {
        cur.addFile(t2, parseInt(t1));
      }
    }
  });

const diskSize = 70000000;
const diskNeeded = 30000000;
const diskTarget = root.size - (diskSize - diskNeeded);

// root.print();

console.log(root.findClosestDirectorySize(diskTarget));
