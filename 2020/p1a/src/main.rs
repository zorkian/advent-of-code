use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;

fn main() {
    let mut nums = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(number) = line {
                let int = number.parse::<u32>().unwrap();
                nums.insert(int);
            }
        }
    }

    for num in &nums {
        let target = 2020-num;
        if nums.contains(&target) {
            println!("{} * {} = {}", num, target, num*target)
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
