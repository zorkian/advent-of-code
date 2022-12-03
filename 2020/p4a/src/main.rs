use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let mut valid_ct = 0;
    let mut passport = HashSet::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // hgt:161cm eyr:2027
                // ecl:grn iyr:2011 hcl:#a97842 byr:1977 pid:910468396

                let parts: Vec<&str> = lin.split(" ").collect();
                if parts.len() == 1 && parts[0] == "" {
                    // Complete passport, validate it
                    if passport.len() == 8 || (passport.len() == 7 && !passport.contains("cid")) {
                        valid_ct += 1;
                    }

                    passport.clear();
                } else {
                    // New things, insert the parts
                    for part in parts {
                        let kvparts: Vec<&str> = part.split(":").collect();
                        passport.insert(String::from(kvparts[0]));
                    }
                }
            }
        }
    }

    println!("valid = {}", valid_ct)
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
