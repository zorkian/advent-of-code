use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut flight = [[0u8; 8]; 128];

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // 70 = F, 66 = B
                let parts = lin.as_bytes();
                let mut row = 0;
                let mut height = 128;
                for i in 0..8 {
                    height /= 2;
                    if parts[i] == 66 {
                        row += height;
                    }
                }

                // 76 = L, 82 == R
                let mut col = 0;
                let mut width = 8;
                for i in 0..3 {
                    width /= 2;
                    if parts[i + 7] == 82 {
                        col += width;
                    }
                }

                flight[row][col] = 1;
            }
        }
    }

    for row in 0..128 {
        print!("{} ", row);
        for col in 0..8 {
            print!("{}", flight[row][col]);
        }
        println!("");
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
