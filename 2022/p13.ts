import { assert } from "console";
import * as fs from "fs";

// BOILERPLATE HERE

const { program } = require("commander");

program.option("-p1").option("-p2").option("-sample");
program.parse();

const options = program.opts();
const filename = "inputs/day13." + (options.Sample ? "sample" : "input");

const lines = fs.readFileSync(filename, "utf8").split(/\r?\n\r?\n/);

// PARSING LIZARDS HERE

// [] => Element is_array no contents
class Element {
  is_array: boolean = false;
  value: number = 0;
  items: Array<Element> = new Array();
  marker: number = 0;

  repr(): string {
    var str = "";
    if (!this.is_array) {
      str += this.value;
      return str;
    }
    this.items.forEach((elem) => (str += (str != "" ? "," : "") + elem.repr()));
    return "[" + str + "]";
  }

  _fill(input: string, base: boolean): string {
    // [1,[2,[3,[4,[5,6,7]]]],8,9]
    // console.log("_fill:", input, base);

    if (base) {
      this.is_array = true;
    }

    var str = "";
    while (input != "") {
      var chr = input.charAt(0);
      input = input.substring(1, input.length);

      if (chr == "[") {
        // I am now an array, if this is not the first call, insert a new element
        // and begin parsing from that point
        if (base) {
          base = false;
          continue;
        }

        // Pass this off to a new element to parse, it will return any unconsumed
        // stuff after the ] it encounters
        // console.log("pushing [", input);
        var elem = new Element();
        elem.is_array = true;
        input = elem._fill(input, false);
        this.items.push(elem);
      } else if (chr == "," || chr == "]") {
        // If we have a number, now parse it and insert it into the current element's
        // list of items
        if (str != "") {
          var elem = new Element();
          elem.value = parseInt(str.trim());
          this.items.push(elem);
          str = "";
        }
        if (chr == "]") {
          // If we are seeing this, that means we're done parsing and can return
          // up to the prior caller with anything that's left in input
          // console.log("closing", input);
          return input;
        }
      } else {
        // This is a number, expand remaining
        str += chr;
      }
    }

    return "";
  }

  fill(input: string) {
    this._fill(input, true);
    // console.log(this);
  }
}

function parse(lines: Array<string>): Array<Array<string>> {
  var res = new Array();

  lines.forEach((line) => {
    if (!line) return;

    var [l, r] = line.split(/\r?\n/);
    res.push([l, r]);
  });

  return res;
}

// DRAGONS HERE

function inOrder2(l: Element, r: Element): boolean {
  // Must take lists as inputs
  if (!(l.is_array && r.is_array)) {
    throw "not both lists";
  }

  // Now iterate the items
  for (var idx = 0; idx < l.items.length; idx++) {
    if (idx >= r.items.length) {
      // console.log("right out of items");
      return false;
    }

    var li = l.items[idx];
    var ri = r.items[idx];

    // console.log("LEFT:", li.repr());
    // console.log("RITE:", ri.repr());

    // If one is a list and the other isn't, promote the non-list into
    // a simple list, then do a recursive compare
    var promoted = false;
    if (li.is_array && !ri.is_array) {
      // console.log("promotion right");
      ri.is_array = true;
      var elem = new Element();
      elem.value = ri.value;
      ri.items.push(elem);
      ri.value = 0;
      promoted = true;
    } else if (ri.is_array && !li.is_array) {
      // console.log("promotion left");
      li.is_array = true;
      var elem = new Element();
      elem.value = li.value;
      li.items.push(elem);
      li.value = 0;
      promoted = true;
    }

    // If lists, do recursion
    if (li.is_array && ri.is_array) {
      return inOrder2(li, ri);
    } else if (!(li.is_array && ri.is_array)) {
      if (li.value == ri.value) {
        continue;
      }
      // console.log("numeric comparison", li.value, ri.value);
      return li.value <= ri.value;
    } else {
      throw "unknown compare state";
    }
  }

  // If we're here, we're gucci (left out of items and nothing was wrong)
  // console.log("truthfulness");
  return true;
}

function inOrder(l: Element, r: Element, base: boolean): boolean {
  console.log("enter");

  // If left list is out of elements, we're in order
  if (l.is_array && l.items.length == 0) {
    console.log("left out of elems, TRUE");
    return true;
  }

  // If right is out of elements, out of order
  if (r.is_array && r.items.length == 0) {
    console.log("right out of elems");
    return false;
  }

  // If both are bare integers... simple compare and return.
  if (!(l.is_array || r.is_array)) {
    console.log("c2 int compare", l.value, r.value);
    return l.value <= r.value;
  }

  // If we have a bare integer opposite a list, promote the integer into
  // a single element list for the below logic
  if (l.is_array && !r.is_array) {
    r.is_array = true;
    var elem = new Element();
    elem.value = r.value;
    r.items.push(elem);
    r.value = 0;
  } else if (r.is_array && !l.is_array) {
    l.is_array = true;
    var elem = new Element();
    elem.value = l.value;
    l.items.push(elem);
    l.value = 0;
  }

  // Now compare by iterating the items and recursively doing a comparison
  // on those, if we ever get a false then we're done, or if we run out of
  // items on one side
  for (var idx = 0; idx < l.items.length; idx++) {
    if (idx >= r.items.length) {
      // If this is a base case, it's bad that the right ran out,
      // but if we're within a list, it's not
      console.log("base compare", !base);
      return !base;
    }
    var rv = inOrder(l.items[idx], r.items[idx], false);
    if (!rv) {
      console.log("sub-compare false");
      return false;
    }
  }

  // If we get here, we believe we're still in order, and we don't need
  // to check the remaining right side items
  console.log("overall true");
  return true;
}

function part1(lines: Array<string>): number {
  var input = parse(lines);

  var idx = 0;
  var score = 0;
  input.forEach((pair) => {
    idx++;

    var lp = new Element();
    lp.fill(pair[0]);
    // console.log(pair[0]);
    // console.log(lp.repr());

    var rp = new Element();
    rp.fill(pair[1]);
    // console.log(pair[1]);
    // console.log(rp.repr());

    if (inOrder2(lp, rp)) {
      // console.log(idx, "inorder:", pair[0], pair[1]);
      score += idx;
    } else {
      // console.log(idx, "outorder:", pair[0], pair[1]);
    }
  });
  return score;
}

// HARDCORE DRAGONS HERE

function part2(lines: Array<string>): number {
  var input = parse(lines);

  var elems: Array<Element> = new Array();

  input.forEach((pair) => {
    var lp = new Element();
    lp.fill(pair[0]);

    var rp = new Element();
    rp.fill(pair[1]);

    elems.push(lp);
    elems.push(rp);
  });

  var t = new Element();
  t.fill("[[6]]");
  t.marker = 6;
  elems.push(t);

  t = new Element();
  t.fill("[[2]]");
  t.marker = 2;
  elems.push(t);

  elems.sort((a, b) => (inOrder2(a, b) ? -1 : 1));
  // elems.forEach((elem) => console.log(elem.repr()));

  var idx2 = 0,
    idx6 = 0;
  for (var idx = 0; idx < elems.length; idx++) {
    if (elems[idx].marker == 2) {
      idx2 = idx + 1;
    }
    if (elems[idx].marker == 6) {
      idx6 = idx + 1;
    }
  }
  return idx2 * idx6;
}

// DO IT

console.log(options.P1 ? part1(lines) : part2(lines));
