use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;
    let mut answers = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                let bytes = lin.as_bytes();
                if bytes.len() == 0 {
                    println!("group had {} answers", answers.len());
                    valid_ct += answers.len();
                    answers.clear();
                } else {
                    // New things, insert the answers
                    for byte in bytes {
                        if byte >= &97u8 && byte <= &122u8 {
                            answers.insert(*byte);
                        }
                    }
                }
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
