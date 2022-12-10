import * as fs from "fs";

var score: number = 0;

// Current register value
var regX: number = 1;

// Index into the array is for "start of sample" point in time,
// ergo, samples[0] = "at the beginning of/during the first cycle"
var samples: Array<number> = new Array();

fs.readFileSync("inputs/day10.input", "utf8")
  .split(/\r?\n/)
  .forEach((line) => {
    if (!line) return;

    if (line == "noop") {
      samples.push(regX);
    } else {
      var [_, p2] = line.split(/ /);
      var ct = parseInt(p2);

      samples.push(regX);
      samples.push(regX);
      regX += ct;
    }

    //console.log(line, " => ", regX, " [", samples.length, "]");
  });

for (var ct = 20; ct < samples.length; ct += 40) {
  //console.log(ct, samples[ct - 1]);
  score += ct * samples[ct - 1];
}

for (var ct = 0; ct < samples.length; ct++) {
  //console.log(ct, ":", samples[ct]);
}

console.log(score);
