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

    // console.log(line, " => ", regX, " [", samples.length, "]");
  });

var scanline: string = "";
for (var ct = 0; ct < samples.length; ct++) {
  if (ct >= 40 && ct % 40 == 0) {
    console.log(scanline);
    scanline = "";
  }

  if (samples[ct] >= (ct % 40) - 1 && samples[ct] <= (ct % 40) + 1) {
    scanline += "#";
  } else {
    scanline += ".";
  }
}
console.log(scanline);
