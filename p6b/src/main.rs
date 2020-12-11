use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;
    let mut initial = true;
    let mut answers = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                let bytes = lin.as_bytes();
                if bytes.len() == 0 {
                    valid_ct += answers.len();
                    answers.clear();
                    initial = true;
                } else {
                    // New things, insert the answers
                    let mut new_answers = HashSet::new();
                    for byte in bytes {
                        let b = *byte;
                        if b >= 97 && b <= 122 {
                            new_answers.insert(b);
                        }
                    }

                    if initial {
                        for answer in new_answers {
                            &answers.insert(answer);
                        }
                        initial = false;
                    } else {
                        let mut remove: Vec<u8> = Vec::new();
                        for answer in &answers {
                            if !new_answers.contains(&answer) {
                                remove.push(*answer);
                            }
                        }
                        for answer in remove {
                            answers.remove(&answer);
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
