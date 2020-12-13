use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut sidx: usize = 0;
    let mut eidx: usize = 0;
    let mut sum: u64 = 0;
    let target_number: u64 = 22406676;
    let mut numbers: VecDeque<u64> = VecDeque::new();
    let mut number_set: HashSet<u64> = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                let number = lin.parse::<u64>().unwrap();
                numbers.push_back(number);
            }
        }
    }

    // initialize to "continugous set of first number"
    sum = numbers[0];

    loop {
        if sum == target_number {
            let mut smallest = numbers[sidx];
            let mut largest = numbers[eidx];
            for i in sidx..eidx {
                if numbers[i] < smallest {
                    smallest = numbers[i]
                } else if numbers[i] > largest {
                    largest = numbers[i]
                }
            }

            println!(
                "start {} {} end {} {} = {}",
                sidx,
                smallest,
                eidx,
                largest,
                smallest + largest
            );
            break;
        } else if sum < target_number {
            eidx += 1;
            sum += numbers[eidx];
        } else if sum > target_number {
            sum -= numbers[sidx];
            sidx += 1;
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
