use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut ts: u32 = 0;

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                if ts == 0 {
                    ts = lin.parse::<u32>().unwrap();
                    continue;
                }

                let parts: Vec<&str> = lin.split(",").collect();
                let mut buses: Vec<u32> = Vec::new();
                for part in parts {
                    if part == "x" {
                        continue;
                    }
                    buses.push(part.parse::<u32>().unwrap());
                }

                let mut lowest_ts: u32 = 0;
                let mut lowest_bus: u32 = 0;
                for bus in buses {
                    let mut next_ts: f64 = (ts as f64) / (bus as f64);
                    next_ts = next_ts.trunc() as f64 + 1f64;
                    next_ts *= bus as f64;

                    let next_ts_int: u32 = next_ts as u32;
                    if lowest_ts == 0 || next_ts_int < lowest_ts {
                        lowest_ts = next_ts_int;
                        lowest_bus = bus;
                    }
                }

                println!("lowest bus {} time {}", lowest_bus, lowest_ts - ts);
            }
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
