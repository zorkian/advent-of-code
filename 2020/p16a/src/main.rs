use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug)]
struct Pair {
    lower: u16,
    upper: u16,
}

fn add_range(ranges: &mut Vec<Pair>, lower: u16, upper: u16) {
    dbg!(&ranges);
    let mut was_inserted = false;
    for idx in 0..ranges.len() {
        // If this range is totally below current pointer, insert here
        if upper < ranges[idx].lower {
            was_inserted = true;
            ranges.insert(
                idx,
                Pair {
                    lower: lower,
                    upper: upper,
                },
            );
            println!(
                "inserted new range {}, {} below index {}",
                lower, upper, idx
            );
        } else if lower >= ranges[idx].lower && upper <= ranges[idx].upper {
            // Range is totally inside other range, ignore it
            was_inserted = true;
            println!(
                "range {}, {} combined with range {}, {} by being swallowed",
                lower, upper, ranges[idx].lower, ranges[idx].upper
            );
        } else if lower < ranges[idx].lower && upper <= ranges[idx].upper {
            // Else, if this range is below but extends into the range, just expand
            // the existing range downward
            was_inserted = true;
            println!(
                "range {}, {} combined with range {}, {} by lowering",
                lower, upper, ranges[idx].lower, ranges[idx].upper
            );
            ranges[idx].lower = lower;
        } else if lower <= ranges[idx].upper && upper > ranges[idx].upper {
            // Else, see if this range overlaps the top and could be extended
            was_inserted = true;
            println!(
                "range {}, {} combined with range {}, {} by raising",
                lower, upper, ranges[idx].lower, ranges[idx].upper
            );
            ranges[idx].upper = upper;
        }

        if was_inserted {
            return;
        }
    }

    if !was_inserted {
        // Empty case or was too big
        ranges.push(Pair {
            lower: lower,
            upper: upper,
        });
        println!("inserted new range {}, {}", lower, upper);
    }
}

fn main() {
    let mut errors = 0;
    let mut ranges: Vec<Pair> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        let mut section = 0;
        for line in lines {
            if let Ok(lin) = line {
                if lin == "your ticket:" {
                    section = 1;
                    continue;
                } else if lin == "nearby tickets:" {
                    section = 2;
                    continue;
                } else if lin == "" {
                    continue;
                }
                if section == 0 {
                    let parts: Vec<&str> = lin.split(": ").collect();
                    let aranges: Vec<&str> = parts[1].split(" or ").collect();
                    for range in aranges {
                        let lrange: Vec<&str> = range.split("-").collect();
                        let lower = lrange[0].parse::<u16>().unwrap();
                        let upper = lrange[1].parse::<u16>().unwrap();
                        add_range(&mut ranges, lower, upper)
                    }
                } else if section == 1 {
                    // skip for now
                } else if section == 2 {
                    let parts: Vec<&str> = lin.split(",").collect();
                    for part in parts {
                        let number = part.parse::<u16>().unwrap();
                        if number < 28 || number > 974 {
                            errors += number;
                        }
                    }
                }
            }
        }
    }
    dbg!(errors);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
