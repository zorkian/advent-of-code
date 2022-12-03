use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // 1-3 c: cctdcvcdqc
                let parts: Vec<&str> = lin.split(" ").collect();

                let minmax: Vec<&str> = parts[0].split("-").collect();
                let min = minmax[0].parse::<usize>().unwrap();
                let max = minmax[1].parse::<usize>().unwrap();

                let valid = parts[1].as_bytes()[0];

                let pass = parts[2].as_bytes();
                if (pass[min-1] == valid) ^ (pass[max-1] == valid) {
                    valid_ct += 1;
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
