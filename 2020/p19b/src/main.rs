extern crate regex;

use regex::Regex;
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut tmp_rules: HashMap<u32, String> = HashMap::new();
    let mut rules: HashMap<u32, String> = HashMap::new();
    let mut patterns: Vec<String> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        let mut pattern_time = false;
        for line in lines {
            if let Ok(lin) = line {
                // If blank line, switch to test pattern insertion
                if pattern_time || lin == "" {
                    patterns.push(String::from(lin));
                    pattern_time = true;
                    continue;
                }

                let parts: Vec<&str> = lin.split(": ").collect();

                // Special case: base rules are just 'a' or 'b', so add those
                // to the parsed rules
                if parts[1] == "\"a\"" {
                    rules.insert(parts[0].parse::<u32>().unwrap(), String::from("a"));
                } else if parts[1] == "\"b\"" {
                    rules.insert(parts[0].parse::<u32>().unwrap(), String::from("b"));
                } else {
                    tmp_rules.insert(parts[0].parse::<u32>().unwrap(), String::from(parts[1]));
                }
            }
        }
    }

    // Iterate the rules until they've all been expanded into actual rules
    loop {
        if tmp_rules.len() == 0 {
            break;
        }

        for (id, rule_definition) in &tmp_rules {
            let mut all_valid = true;
            let mut outer_re: String = "(?:".to_owned();
            let mut prepend_alternator = false;
            for rule in rule_definition.split(" | ") {
                if prepend_alternator {
                    outer_re.push_str("|");
                }
                let mut temp_re: String = "".to_owned();
                for rule_id in rule.split(" ") {
                    let test_rule_id = rule_id.parse::<u32>().unwrap();
                    if rules.contains_key(&test_rule_id) {
                        temp_re.push_str(rules.get(&test_rule_id).unwrap());
                    } else {
                        all_valid = false;
                    }
                }
                outer_re.push_str(&temp_re);
                prepend_alternator = true;
            }
            if !all_valid {
                continue;
            }
            outer_re.push_str(")");

            // Dumb hack
            if !outer_re.contains("|") {
                outer_re = String::from(&outer_re[3..outer_re.len() - 1]);
            }

            // This rule is done, insert it and remove from temp
            // println!("rule {} = {}", id, &outer_re);
            rules.insert(*id, outer_re);
        }

        // Remove rules from tmp
        for id in rules.keys() {
            tmp_rules.remove(id);
        }

        // Insert hack rules if necessary
        if !rules.contains_key(&8) && rules.contains_key(&42) {
            // Rule 8 is 42 repeated 1 or more times
            let mut tmp: String = "".to_owned();
            tmp.push_str(rules.get(&42).unwrap());
            tmp.push_str("+?");
            rules.insert(8, tmp);
        }
        if !rules.contains_key(&11) && rules.contains_key(&42) && rules.contains_key(&31) {
            // Rule 11 is some number of 42 repeats, plus the same number
            // of 31 repeats
            let mut tmp: String = "(?P<Z>(?P<A>".to_owned();
            tmp.push_str(rules.get(&42).unwrap());
            tmp.push_str("+)(?P<B>");
            //tmp.push_str("(?-1)");
            tmp.push_str(rules.get(&31).unwrap());
            tmp.push_str("+))");
            dbg!(&tmp);
            rules.insert(11, tmp);
        }
    }

    // Compile the monster
    let mut rule0: String = "^".to_owned();
    rule0.push_str(rules.get(&0).unwrap());
    rule0.push_str("$");

    let re = Regex::new(&rule0).unwrap();
    let re42 = Regex::new(rules.get(&42).unwrap()).unwrap();
    dbg!(rules.get(&42).unwrap());
    let re31 = Regex::new(rules.get(&31).unwrap()).unwrap();
    dbg!(rules.get(&31).unwrap());

    // Now iterate patterns, testing pattern 0
    let mut valid_ct = 0;
    for pattern in patterns {
        match re.captures(&pattern) {
            Some(capture) => {
                let cz = capture.name("Z").unwrap();
                dbg!(&cz.as_str());
                let ca = capture.name("A").unwrap();
                dbg!(&ca.as_str());
                let cb = capture.name("B").unwrap();
                dbg!(&cb.as_str());

                // Attempt to do balanced matching of 42/31 pairs
                // by constructing regexes manually, this is kind of gross
                // but hey
                // let mut any_valid = false;
                // for i in 1..10 {
                //     let mut tmp: String = "^".to_owned();
                //     tmp.push_str(rules.get(&42).unwrap());
                //     tmp.push_str(&format!("{{{}}}", i));
                //     tmp.push_str(rules.get(&31).unwrap());
                //     tmp.push_str(&format!("{{{}}}$", i));

                //     let tmpre = Regex::new(&tmp).unwrap();
                //     if tmpre.is_match(cz.as_str()) {
                //         println!("matched length {}", i);
                //         any_valid = true;
                //         break;
                //     }
                // }

                // if any_valid {
                //     valid_ct += 1;
                // }

                let c42 = capture.name("A");
                let mut c42_matches = 0;
                match c42 {
                    Some(c42_capture) => {
                        dbg!(c42_capture.as_str());
                        for _i in re42.captures_iter(c42_capture.as_str()) {
                            c42_matches += 1;
                        }
                    }
                    _ => {}
                };
                dbg!(c42_matches);

                let c31 = capture.name("B");
                let mut c31_matches = 0;
                match c31 {
                    Some(c31_capture) => {
                        dbg!(c31_capture.as_str());
                        for _i in re31.captures_iter(c31_capture.as_str()) {
                            c31_matches += 1;
                        }
                    }
                    _ => {}
                };
                dbg!(c31_matches);

                //println!("{} MATCHES", pattern);
                if c42_matches > c31_matches {
                    valid_ct += 1
                }
            }
            _ => println!("{} DOES NOT MATCH", pattern),
        }
    }

    dbg!(valid_ct);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
