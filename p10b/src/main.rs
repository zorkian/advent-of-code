use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn chain(
    cache: &mut HashMap<usize, u64>,
    numbers: &Vec<u64>,
    cur_jolt_idx: usize,
    target_jolts: u64,
) -> u64 {
    // If in cache, return it
    match cache.get(&cur_jolt_idx) {
        Some(result) => return *result,
        None => {}
    };

    let mut counter: u64 = 0;
    //println!("chain({}, {})", cur_jolt_idx, target_jolts);

    // Get current joltage
    let cur_joltage = numbers[cur_jolt_idx];
    let max_joltage = cur_joltage + 3;

    // Find valid connections
    for i in cur_jolt_idx + 1..numbers.len() {
        if numbers[i] > max_joltage {
            break;
        }

        // Recurse using this one
        counter += chain(cache, numbers, i, target_jolts)
    }

    // Last check, if we can reach the target from here, this is a valid
    // chain and should be counted
    if cur_joltage + 3 >= target_jolts {
        counter += 1
    }

    // Insert into cache
    cache.insert(cur_jolt_idx, counter);
    return counter;
}

fn main() {
    let mut valid_ct = 0;
    let mut numbers: Vec<u64> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                numbers.push(lin.parse::<u64>().unwrap())
            }
        }
    }

    numbers.sort();

    let target_jolts: u64 = numbers[numbers.len() - 1] + 3;

    // Have to kick off chains from each valid initial adaptor
    let mut counter: u64 = 0;
    let mut cache: HashMap<usize, u64> = HashMap::new();
    for i in 0..3 {
        if numbers[i] <= 3 {
            counter += chain(&mut cache, &numbers, i, target_jolts)
        }
    }
    println!("final total: {}", counter)
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
