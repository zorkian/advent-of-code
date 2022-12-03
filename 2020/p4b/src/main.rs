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
                        let key = String::from(kvparts[0]);
                        let value = String::from(kvparts[1]);
                        if validate(&key, &value) {
                            passport.insert(key);
                        } else {
                            println!("key {} = value {} FAILS", key, value);
                        }
                    }
                }
            }
        }
    }

    println!("valid = {}", valid_ct)
}

fn validate(key: &String, value: &String) -> bool {
    if key == "ecl" {
        let ecls = vec!["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];
        return ecls.contains(&value.as_str());
    } else if key == "hcl" {
        let bytes = value.as_bytes();
        if bytes.len() == 7 && bytes[0] == 35 {
            for i in 1..7 {
                if !((bytes[i] >= 48 && bytes[i] <= 57) || (bytes[i] >= 97 && bytes[i] <= 102)) {
                    return false;
                }
            }
            return true;
        }
        return false;
    } else if key == "byr" {
        let int = value.parse::<u16>().unwrap();
        return int >= 1920 && int <= 2002;
    } else if key == "iyr" {
        let int = value.parse::<u16>().unwrap();
        return int >= 2010 && int <= 2020;
    } else if key == "eyr" {
        let int = value.parse::<u16>().unwrap();
        return int >= 2020 && int <= 2030;
    } else if key == "hgt" {
        let bytes = value.as_bytes();
        if bytes.len() == 4 {
            if !(bytes[2] == 105 && bytes[3] == 110) {
                return false;
            }
            let hgt = (bytes[0] - 48) * 10 + (bytes[1] - 48);
            return hgt >= 59 && hgt <= 76;
        } else if bytes.len() == 5 {
            if !(bytes[0] == 49 && bytes[3] == 99 && bytes[4] == 109) {
                return false;
            }
            let hgt = 100 + (bytes[1] - 48) * 10 + (bytes[2] - 48);
            return hgt >= 150 && hgt <= 193;
        }
        return false;
    } else if key == "pid" {
        let bytes = value.as_bytes();
        if bytes.len() == 9 {
            for i in 0..9 {
                if !(bytes[i] >= 48 && bytes[i] <= 57) {
                    return false;
                }
            }
            return true;
        }
        return false;
    } else if key == "cid" {
        return true;
    }
    return false;
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
