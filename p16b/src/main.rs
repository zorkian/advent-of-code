use std::collections::HashMap;
use std::collections::HashSet;
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

fn matches(number: u16, ranges: &Vec<Pair>) -> bool {
    for range in ranges {
        if number >= range.lower && number <= range.upper {
            return true;
        }
    }
    return false;
}

fn main() {
    let mut classes: HashMap<String, Vec<Pair>> = HashMap::new();
    let mut my_ticket: Vec<HashSet<String>> = Vec::new();
    let mut my_ticket_vals: Vec<u16> = Vec::new();
    let mut tickets: Vec<Vec<HashSet<String>>> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        let mut section = 0;
        for line in lines {
            if let Ok(lin) = line {
                if lin == "your ticket:" {
                    section = 1;
                } else if lin == "nearby tickets:" {
                    section = 2;
                } else if lin == "" {
                } else if section == 0 {
                    let parts: Vec<&str> = lin.split(": ").collect();
                    let mut ranges = classes.entry(String::from(parts[0])).or_insert(Vec::new());

                    let aranges: Vec<&str> = parts[1].split(" or ").collect();
                    for range in aranges {
                        let lrange: Vec<&str> = range.split("-").collect();
                        let lower = lrange[0].parse::<u16>().unwrap();
                        let upper = lrange[1].parse::<u16>().unwrap();
                        add_range(&mut ranges, lower, upper)
                    }
                } else {
                    // Otherwise this is a ticket, might be mine or someone else's,
                    // so let's parse it first and calculate the sets that match
                    // for each of the numbers
                    let parts: Vec<&str> = lin.split(",").collect();
                    let mut fields: Vec<HashSet<String>> = Vec::new();
                    let mut all_valid = true;
                    for part in parts {
                        let number = part.parse::<u16>().unwrap();
                        if section == 1 {
                            my_ticket_vals.push(number);
                        }

                        // Iterate all the types of things and see if they match
                        let mut matched_classes: HashSet<String> = HashSet::new();
                        for (class, ranges) in &classes {
                            if matches(number, &ranges) {
                                matched_classes.insert(String::from(class));
                            }
                        }
                        if matched_classes.len() == 0 {
                            all_valid = false;
                        } else {
                            fields.push(matched_classes);
                        }
                    }
                    // If they were all valid, use this row
                    if all_valid {
                        if section == 1 {
                            my_ticket = fields;
                        } else {
                            if fields.len() != my_ticket.len() {
                                panic!("invalid ticket seems valid?");
                            }

                            // Intersect against my ticket
                            for idx in 0..my_ticket.len() {
                                let intersect: Vec<String> = fields[idx]
                                    .intersection(&my_ticket[idx])
                                    .map(|f| f.clone())
                                    .collect();
                                my_ticket[idx] = HashSet::new();
                                for field in intersect {
                                    my_ticket[idx].insert(field);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // my_ticket now contains a bunch of sets which we know are valid,
    // but we need to find which ones are unique and do that until we
    // have all unique sets
    let mut already_found: HashSet<String> = HashSet::new();
    let mut value: u64 = 1;
    while already_found.len() != my_ticket.len() {
        for idx in 0..my_ticket.len() {
            let difference: HashSet<String> = my_ticket[idx]
                .difference(&already_found)
                .map(|f| f.clone())
                .collect();
            if difference.len() != 1 {
                continue;
            }
            // Ok, we know that this field is the one item, add it to our
            // subtractive set and continue
            let found_element = difference.iter().take(1).next().unwrap();
            println!("Field {} is '{}'", idx + 1, found_element);
            if found_element.starts_with("departure ") {
                value *= my_ticket_vals[idx] as u64;
            }
            already_found.insert(found_element.clone());
        }
    }
    println!("value = {}", value);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
