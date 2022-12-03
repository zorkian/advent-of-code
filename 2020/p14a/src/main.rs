use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut memory: HashMap<u64, u64> = HashMap::new();

    if let Ok(lines) = read_lines("input.txt") {
        let mut mask_out: u64 = 0;
        let mut mask_or: u64 = 0;

        for line in lines {
            if let Ok(lin) = line {
                // mask = X011X00011011110001X01010011X0X0X010
                // [src/main.rs:30] mask = 49625125802
                // mem[35176] = 9976167
                dbg!(&lin);
                let parts: Vec<&str> = lin.split(" ").collect();

                if parts[0] == "mask" {
                    mask_out = 0;
                    mask_or = 0;

                    let mut idx: u32 = 36;
                    for byte in parts[2].as_bytes() {
                        idx -= 1;
                        match *byte {
                            48 => {}
                            49 => mask_or += 1 << idx,
                            88 => mask_out += 1 << idx,
                            _ => panic!("oh god"),
                        }
                    }
                    dbg!(mask_out);
                    dbg!(mask_or);
                } else {
                    let index = dbg!(parts[0][4..parts[0].len() - 1].parse::<u64>().unwrap());
                    let mut val = dbg!(parts[2].parse::<u64>().unwrap());
                    *memory.entry(index).or_default() = dbg!(val & mask_out | mask_or);
                }
            }
        }
    }

    let mut sum: u64 = 0;
    for (k, v) in memory {
        println!("[{}] {}", k, v);
        sum += v;
    }

    println!("valid = {}", sum)
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
