use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

const INACTIVE: u8 = 46; // .
const ACTIVE: u8 = 35; // #

const MIN_Z: i8 = -10;
const MAX_Z: i8 = 10;
const MULTIPLIER: usize = 5;

type Board = Vec<u8>;
type Cube = HashMap<i8, Board>;

fn main() {
    let mut cube: Cube = HashMap::new();
    let mut width: usize = 0;
    let mut height: usize = 0;

    // insert boards
    for i in MIN_Z..MAX_Z + 1 {
        cube.entry(i).or_insert(Vec::new());
    }

    let mut temp_board: Board = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                height += 1;

                let parts = lin.as_bytes();
                if width == 0 {
                    width = parts.len();
                }
                for byte in parts {
                    temp_board.push(*byte);
                }
            }
        }
    }

    // Put the board we read into a NxN version of itself
    for _i in 0..width * MULTIPLIER * height * ((MULTIPLIER - 1) / 2) {
        cube.entry(0).or_default().push(INACTIVE);
    }
    // Middle is annoying
    let copies = ((MULTIPLIER - 1) / 2) * width;
    for y in 0..height {
        for _x in 0..copies {
            cube.entry(0).or_default().push(INACTIVE);
        }
        for x in 0..width {
            cube.entry(0).or_default().push(temp_board[y * width + x]);
        }
        for _x in 0..copies {
            cube.entry(0).or_default().push(INACTIVE);
        }
    }
    for _i in 0..width * MULTIPLIER * height * ((MULTIPLIER - 1) / 2) {
        cube.entry(0).or_default().push(INACTIVE);
    }

    // Expand width/height
    width *= MULTIPLIER;
    height *= MULTIPLIER;

    // fill up boards
    for i in MIN_Z..MAX_Z + 1 {
        dbg!(cube[&i].len());
        if cube[&i].len() < width * height {
            for _ct in 0..width * height {
                cube.entry(i).or_default().push(INACTIVE);
            }
        }
    }

    for _i in 0..6 {
        simulate(&mut cube, width, height);
    }

    //println!("stasis reached at turn {}", count);

    let mut actives = 0;
    for (_zindex, board) in cube {
        for tile in &board {
            if *tile == ACTIVE {
                actives += 1
            }
        }
    }
    println!("occupied actives {}", actives);
}

fn num_occupied(cube: &Cube, tx: usize, ty: usize, tz: i8, width: usize, height: usize) -> usize {
    let mut active = 0;

    let mut min_x = tx;
    if min_x > 0 {
        min_x -= 1
    }

    let mut min_y = ty;
    if min_y > 0 {
        min_y -= 1;
    }

    let min_z = tz - 1;
    if min_z < MIN_Z {
        panic!("need more negative z");
    } else if tz + 1 > MAX_Z {
        panic!("need more positive z");
    }

    for z in min_z..tz + 2 {
        for y in min_y..ty + 2 {
            for x in min_x..tx + 2 {
                if x == tx && y == ty && z == tz {
                    continue;
                }
                if x < width && y < height {
                    if cube.contains_key(&z) {
                        // println!(
                        //     "{},{},{} > {},{},{} = {}",
                        //     tx,
                        //     ty,
                        //     tz,
                        //     x,
                        //     y,
                        //     &z,
                        //     cube[&z][y * width + x]
                        // );
                        if cube[&z][y * width + x] == ACTIVE {
                            active += 1;
                        }
                    }
                }
            }
        }
    }
    // dbg!(active);
    return active;
}

fn simulate(cube: &mut Cube, width: usize, height: usize) -> bool {
    let mut any_changed = false;
    let mut new_cube: Cube = HashMap::new();

    for z in MIN_Z + 1..MAX_Z {
        let board = cube.get(&z).unwrap();
        let mut new_board: Board = Vec::with_capacity(board.len());

        println!("Z: {}", z);
        for y in 0..height {
            println!(
                "{}",
                String::from_utf8(board[y * width..y * width + width].to_vec()).unwrap()
            );

            for x in 0..width {
                let occupied = num_occupied(cube, x, y, z, width, height);
                match board[y * width + x] {
                    INACTIVE => {
                        if occupied == 3 {
                            new_board.push(ACTIVE);
                            any_changed = true;
                        } else {
                            new_board.push(INACTIVE)
                        }
                    }
                    ACTIVE => {
                        if occupied < 2 || occupied > 3 {
                            new_board.push(INACTIVE);
                            any_changed = true;
                        } else {
                            new_board.push(ACTIVE)
                        }
                    }
                    _ => {
                        panic!("invalid tile contents")
                    }
                }
            }
        }

        if board.len() != new_board.len() {
            dbg!(board.len());
            dbg!(new_board.len());
            panic!("boards misshaped");
        }

        new_cube.entry(z).or_insert(new_board);
    }

    for (zindex, board) in &new_cube {
        cube.insert(*zindex, board.clone());
    }

    return !any_changed;
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
