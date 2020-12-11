use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut nums = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(number) = line {
                let int = number.parse::<i32>().unwrap();
                nums.insert(int);
            }
        }
    }

    for num in &nums {
        for num2 in &nums {
            if num != num2 {
                let target = 2020 - num - num2;
                if nums.contains(&target) {
                    println!("{} * {} * {} = {}", num, num2, target, num * num2 * target)
                }
            }
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
