use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;
    let mut numbers: Vec<u32> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                numbers.push(lin.parse::<u32>().unwrap())
            }
        }
    }

    numbers.sort();

    let mut counts: HashMap<u32, u32> = HashMap::new();
    let mut last_num: u32 = 0;
    for num in numbers {
        let diff = num - last_num;
        *counts.entry(diff).or_insert(0) += 1;

        last_num = num;
    }

    for (diff, count) in &counts {
        println!("{} is {}", diff, count)
    }

    println!("total is {}", counts[&1] * (counts[&3] + 1))
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
