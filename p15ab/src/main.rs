use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut numbers: HashMap<u64, u64> = HashMap::new();
    let mut last_number: u64 = 0;
    let mut turn: u64 = 0;

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // 1-3 c: cctdcvcdqc
                let parts: Vec<&str> = lin.split(",").collect();

                for number in parts {
                    turn += 1;
                    if turn > 1 {
                        *numbers.entry(last_number).or_default() = turn;
                    }
                    last_number = number.parse::<u64>().unwrap();
                    dbg!(last_number);
                }
            }
        }
    }

    turn += 1;
    let mut next_number: u64 = 0;

    while turn <= 30000000 {
        // If last number was first spoken, say 0
        let number_turn = *numbers.entry(last_number).or_default();
        if number_turn == 0 {
            next_number = 0;
        } else {
            next_number = turn - number_turn;
        }

        // Do the accounting
        *numbers.entry(last_number).or_default() = turn;
        last_number = next_number;
        turn += 1;
    }
    dbg!(next_number);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
