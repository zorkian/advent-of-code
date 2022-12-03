use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut max_id = 0;

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

                let seat_id = (row * 8) + col;
                println!("{} x {} = {}", row, col, seat_id);
                if seat_id > max_id {
                    max_id = seat_id;
                }
            }
        }
    }

    println!("max id = {}", max_id);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
