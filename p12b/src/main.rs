use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut wx: i32 = 10;
    let mut wy: i32 = -1;

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                let bytes = lin.as_bytes();
                let mut cmd: u8 = bytes[0];
                let mut value: i32 = String::from_utf8(bytes[1..].to_vec())
                    .unwrap()
                    .parse::<i32>()
                    .unwrap();

                // Left rotations are just R rotations plus some
                if cmd == 76 {
                    cmd = 82;
                    value = 360 - value;
                }

                match cmd {
                    78 => wy -= value,
                    83 => wy += value,
                    69 => wx += value,
                    87 => wx -= value,
                    70 => {
                        x += wx * value;
                        y += wy * value;
                    }
                    82 => match value {
                        // R
                        0 => {}
                        90 => {
                            let tmpx = -wy;
                            let tmpy = wx;
                            println!("R90 -> ({}, {}) -> ({}, {})", wx, wy, tmpx, tmpy);
                            wx = tmpx;
                            wy = tmpy;
                        }
                        180 => {
                            let tmpx = -wx;
                            let tmpy = -wy;
                            println!("R180 -> ({}, {}) -> ({}, {})", wx, wy, tmpx, tmpy);
                            wx = tmpx;
                            wy = tmpy;
                        }
                        270 => {
                            let tmpx = wy;
                            let tmpy = -wx;
                            println!("R270 -> ({}, {}) -> ({}, {})", wx, wy, tmpx, tmpy);
                            wx = tmpx;
                            wy = tmpy;
                        }
                        _ => panic!("invalid facing {}", value),
                    },
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
