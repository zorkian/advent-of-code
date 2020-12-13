use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;
    let mut bags: HashMap<String, Vec<String>> = HashMap::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // 1-3 c: cctdcvcdqc
                let parts: Vec<&str> = lin.split(" bags contain ").collect();

                let outer_bag = parts[0];
                if !bags.contains_key(outer_bag) {
                    bags.insert(String::from(outer_bag), vec![]);
                }

                let contains: Vec<&str> = parts[1][..parts[1].len() - 1].split(", ").collect();
                for bag in contains {
                    if bag == "no other bags" {
                        continue;
                    }

                    // get counter and
                    let bag_parts: Vec<&str> = bag.split(" ").collect();
                    let _bag_count = bag_parts[0].parse::<u8>().unwrap();
                    let inner_bag = String::from(bag_parts[1..bag_parts.len() - 1].join(" "));
                    let inner_bag2 = inner_bag.clone();

                    if !bags.contains_key(&inner_bag) {
                        bags.insert(inner_bag, vec![]);
                    }

                    bags.get_mut(&inner_bag2)
                        .unwrap()
                        .push(String::from(outer_bag));
                }
            }
        }
    }

    let mut cur: Vec<&str> = vec!["shiny gold"];
    let mut counted_bags: HashMap<String, bool> = HashMap::new();

    while cur.len() >= 1 {
        let next = cur.pop().unwrap();

        for bag in &bags[next] {
            let bag2 = bag.clone();
            if counted_bags.contains_key(bag) {
                continue;
            }
            valid_ct += 1;
            cur.push(bag);
            counted_bags.insert(bag2, true);
        }
    }

    for (k, v) in bags {
        // println!("{} -> {}", k, v.join(", "));
    }

    println!("valid = {}", valid_ct)
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
