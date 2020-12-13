use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

struct Bag {
    name: String,
    count: u32,
}

fn main() {
    let mut valid_ct = 0;
    let mut bags: HashMap<String, Vec<Bag>> = HashMap::new();

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
                    let inner_bag = String::from(bag_parts[1..bag_parts.len() - 1].join(" "));
                    let my_bag = Bag {
                        name: inner_bag.clone(),
                        count: bag_parts[0].parse::<u32>().unwrap(),
                    };

                    if !bags.contains_key(&inner_bag) {
                        bags.insert(inner_bag, vec![]);
                    }

                    bags.get_mut(outer_bag).unwrap().push(my_bag);
                }
            }
        }
    }

    let mut cur: Vec<Bag> = vec![Bag {
        name: String::from("shiny gold"),
        count: 1,
    }];
    let mut counted_bags: HashMap<String, bool> = HashMap::new();

    while cur.len() >= 1 {
        let this = cur.pop().unwrap();

        for bag in &bags[&this.name] {
            if counted_bags.contains_key(&bag.name) {
                //continue;
            }
            let bag_count = this.count * bag.count;
            valid_ct += bag_count;
            cur.push(Bag {
                name: bag.name.clone(),
                count: bag_count,
            });
            counted_bags.insert(bag.name.clone(), true);
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
