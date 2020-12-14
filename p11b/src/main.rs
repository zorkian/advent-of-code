use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// 46 = ., 76 = L, 36 = #
const SEAT: u8 = 76;
const FLOOR: u8 = 46;
const BODY: u8 = 35;

fn main() {
    let mut board: Vec<u8> = Vec::new();
    let mut width: usize = 0;
    let mut height: usize = 0;

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                height += 1;

                let parts = lin.as_bytes();
                if width == 0 {
                    width = parts.len();
                }
                for byte in parts {
                    board.push(*byte);
                }
            }
        }
    }

    let mut count = 0;
    loop {
        count += 1;
        if simulate(&mut board, width, height) {
            println!("stasis reached at turn {}", count);

            let mut bodies = 0;
            for tile in board {
                if tile == BODY {
                    bodies += 1
                }
            }
            println!("occupied seats {}", bodies);

            break;
        }
    }
}

fn occupied_los(
    board: &Vec<u8>,
    tx: usize,
    ty: usize,
    width: usize,
    height: usize,
    rx: i32,
    ry: i32,
) -> usize {
    let mut x: i32 = tx as i32;
    let mut y: i32 = ty as i32;

    loop {
        x += rx;
        y += ry;

        if x < 0 || x >= width as i32 || y < 0 || y >= height as i32 {
            // Went off edge, unoccupied
            // println!(
            //     "occupied_los({}, {}, {}, {}) went off edge {} {} vs {} {}",
            //     tx, ty, rx, ry, x, y, width, height
            // );
            return 0;
        }

        let tile = board[y as usize * width + x as usize];
        if tile == BODY {
            //println!("occupied_los({}, {}, {}, {}) = 1", tx, ty, rx, ry);
            return 1;
        } else if tile == SEAT {
            //println!("occupied_los({}, {}, {}, {}) = 0", tx, ty, rx, ry);
            return 0;
        }
    }
}

fn num_occupied(board: &Vec<u8>, tx: usize, ty: usize, width: usize, height: usize) -> usize {
    return occupied_los(board, tx, ty, width, height, -1, -1)
        + occupied_los(board, tx, ty, width, height, 0, -1)
        + occupied_los(board, tx, ty, width, height, 1, -1)
        + occupied_los(board, tx, ty, width, height, -1, 0)
        + occupied_los(board, tx, ty, width, height, 1, 0)
        + occupied_los(board, tx, ty, width, height, -1, 1)
        + occupied_los(board, tx, ty, width, height, 0, 1)
        + occupied_los(board, tx, ty, width, height, 1, 1);
}

fn simulate(board: &mut Vec<u8>, width: usize, height: usize) -> bool {
    let mut any_changed = false;
    let mut new_board: Vec<u8> = Vec::with_capacity(board.len());

    println!("");
    for y in 0..height {
        println!(
            "{}",
            String::from_utf8(board[y * width..y * width + width].to_vec()).unwrap()
        );

        for x in 0..width {
            let occupied = num_occupied(board, x, y, width, height);
            match board[y * width + x] {
                SEAT => {
                    if occupied == 0 {
                        new_board.push(BODY);
                        any_changed = true;
                    } else {
                        new_board.push(SEAT)
                    }
                }
                BODY => {
                    if occupied >= 5 {
                        new_board.push(SEAT);
                        any_changed = true;
                    } else {
                        new_board.push(BODY)
                    }
                }
                FLOOR => new_board.push(FLOOR),
                _ => {
                    panic!("invalid tile contents")
                }
            }
        }
    }

    if board.len() != new_board.len() {
        panic!("boards misshaped");
    }

    for i in 0..board.len() {
        board[i] = new_board[i];
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
