use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;
    let mut numbers: VecDeque<u32> = VecDeque::new();
    let mut number_set: HashSet<u32> = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                let number = lin.parse::<u32>().unwrap();

                if numbers.len() < 25 {
                    numbers.push_back(number);
                    number_set.insert(number);
                    continue;
                }

                let mut found = false;
                for test_number in &numbers {
                    if test_number >= &number {
                        continue;
                    }
                    let find_number = number - test_number;
                    if number_set.contains(&find_number) {
                        found = true;
                        break;
                    }
                }

                if !found {
                    println!("{} is not a sum of previous 25!", number);
                    panic!("");
                }

                number_set.remove(&numbers.pop_front().unwrap());
                numbers.push_back(number);
                number_set.insert(number);
            }
        }
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
