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
            println!("rule {} = {}", id, &outer_re);
            rules.insert(*id, outer_re);
        }

        // Remove rules from tmp
        for id in rules.keys() {
            tmp_rules.remove(id);
        }
    }

    // Compile the monster
    let mut rule0: String = "^".to_owned();
    rule0.push_str(rules.get(&0).unwrap());
    rule0.push_str("$");

    let re = Regex::new(&rule0).unwrap();

    // Now iterate patterns, testing pattern 0
    let mut valid_ct = 0;
    for pattern in patterns {
        if re.is_match(&pattern) {
            println!("{} MATCHES", pattern);
            valid_ct += 1;
        } else {
            println!("{} DOES NOT MATCH", pattern);
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
