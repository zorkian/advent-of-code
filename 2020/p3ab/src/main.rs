use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut map: Vec<Vec<u8>> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                map.push(lin.as_bytes().to_vec())
            }
        }
    }

    let width = map[0].len();
    let height = map.len();

    let vert_step = 2;
    let horiz_step = 1;
    let mut hit_tree = 0;
    for i in 1..height {
        if (i % vert_step) == 0 {
            if map[i][(horiz_step * i) % width] == 35 {
                hit_tree += 1;
            }
        }
    }

    println!(
        "right {}, down {} = {} trees",
        horiz_step, vert_step, hit_tree
    )

    // right 1, down 1 = 63 trees
    // right 3, down 1 = 254 trees
    // right 5, down 1 = 62 trees
    // right 7, down 1 = 56 trees
    // right 1, down 2 = 30 trees
    // = 1666768320
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
