use std::cmp;
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

struct World {
    tiles: HashMap<u32, bool>,
    min_x: u8,
    min_y: u8,
    min_z: u8,
    min_w: u8,
    max_x: u8,
    max_y: u8,
    max_z: u8,
    max_w: u8,
}

// const INACTIVE: u8 = 46; // .
const ACTIVE: u8 = 35; // #

fn main() {
    let mut world: World = new_world();

    if let Ok(lines) = read_lines("input.txt") {
        let mut y: u8 = 124;
        for line in lines {
            if let Ok(lin) = line {
                let parts = lin.as_bytes();
                let mut x: u8 = 124;
                for byte in parts {
                    set(&mut world, x, y, 128, 128, *byte == ACTIVE);
                    x += 1;
                }
                y += 1;
            }
        }
    }

    for _i in 0..6 {
        simulate(&mut world);
        //dbg!(&world.tiles);
        dbg!(world.min_x);
        dbg!(world.min_y);
        dbg!(world.min_z);
        dbg!(world.min_w);
        dbg!(world.max_x);
        dbg!(world.max_y);
        dbg!(world.max_z);
        dbg!(world.max_w);
    }

    //println!("stasis reached at turn {}", count);

    let mut actives = 0;
    for tile in world.tiles.values() {
        if *tile {
            actives += 1
        }
    }
    println!("occupied actives {}", actives);
}

fn offset(x: u8, y: u8, z: u8, w: u8) -> u32 {
    return ((x as u32) << 24) + ((y as u32) << 16) + ((z as u32) << 8) + (w as u32);
}

fn set(world: &mut World, x: u8, y: u8, z: u8, w: u8, active: bool) {
    *world.tiles.entry(offset(x, y, z, w)).or_default() = active;
    world.min_x = cmp::min(world.min_x, x - 1);
    world.min_y = cmp::min(world.min_y, y - 1);
    world.min_z = cmp::min(world.min_z, z - 1);
    world.min_w = cmp::min(world.min_w, w - 1);
    world.max_x = cmp::max(world.max_x, x + 1);
    world.max_y = cmp::max(world.max_y, y + 1);
    world.max_z = cmp::max(world.max_z, z + 1);
    world.max_w = cmp::max(world.max_w, w + 1);
}

fn get(world: &World, x: u8, y: u8, z: u8, w: u8) -> bool {
    return *world.tiles.get(&offset(x, y, z, w)).unwrap_or(&false);
}

fn num_occupied(world: &World, tx: u8, ty: u8, tz: u8, tw: u8) -> usize {
    let mut active = 0;

    for w in tw - 1..tw + 2 {
        for z in tz - 1..tz + 2 {
            for y in ty - 1..ty + 2 {
                for x in tx - 1..tx + 2 {
                    if x == tx && y == ty && z == tz && w == tw {
                        continue;
                    }
                    if get(world, x, y, z, w) {
                        active += 1;
                    }
                }
            }
        }
    }
    // println!("{},{},{},{} -> {}", tx, ty, tz, tw, active);
    return active;
}

fn simulate(world: &mut World) {
    let mut temp_world = new_world();

    for w in world.min_w..world.max_w + 1 {
        for z in world.min_z..world.max_z + 1 {
            println!("z={}, w={}", w, z);
            for y in world.min_y..world.max_y + 1 {
                for x in world.min_x..world.max_x + 1 {
                    let occupied = num_occupied(world, x, y, z, w);
                    let is_active = get(world, x, y, z, w);
                    if is_active {
                        print!("#");
                    } else {
                        print!(".");
                    }
                    //print!("{}", occupied);

                    if is_active {
                        set(&mut temp_world, x, y, z, w, !(occupied < 2 || occupied > 3));
                    } else if occupied == 3 {
                        set(&mut temp_world, x, y, z, w, true);
                    } else {
                        set(&mut temp_world, x, y, z, w, false);
                    }
                }
                println!("");
            }
        }
    }

    world.tiles = temp_world.tiles;
    world.min_x = temp_world.min_x;
    world.min_y = temp_world.min_y;
    world.min_z = temp_world.min_z;
    world.min_w = temp_world.min_w;
    world.max_x = temp_world.max_x;
    world.max_y = temp_world.max_y;
    world.max_z = temp_world.max_z;
    world.max_w = temp_world.max_w;
}

fn new_world() -> World {
    return World {
        tiles: HashMap::new(),
        min_x: 128,
        min_y: 128,
        min_z: 128,
        min_w: 128,
        max_x: 128,
        max_y: 128,
        max_z: 128,
        max_w: 128,
    };
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
