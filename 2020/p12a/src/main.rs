use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut facing: i32 = 90; // East

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                let bytes = lin.as_bytes();
                let cmd: u8 = bytes[0];
                let value: i32 = String::from_utf8(bytes[1..].to_vec())
                    .unwrap()
                    .parse::<i32>()
                    .unwrap();

                match cmd {
                    78 => y -= value,
                    83 => y += value,
                    69 => x += value,
                    87 => x -= value,
                    70 => match facing {
                        0 => y -= value,
                        90 => x += value,
                        180 => y += value,
                        270 => x -= value,
                        _ => panic!("invalid facing"),
                    },
                    82 => facing = (facing + value) % 360, // R
                    76 => facing = (facing + (360 - value)) % 360, // L
                    _ => panic!("invalid command"),
                }
            }
        }
    }

    println!("x, y = {}, {} = {}", x, y, x.abs() + y.abs())
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
