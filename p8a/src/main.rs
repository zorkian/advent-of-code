use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug)]
enum CMD {
    Fuck,
    Acc,
    Nop,
    Jmp,
}

struct Instruction {
    cmd: CMD,
    value: i32,
}

fn main() {
    let mut program: Vec<Instruction> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // jmp -44
                let parts: Vec<&str> = lin.split(" ").collect();
                let counter = parts[1].parse::<i32>().unwrap();

                let cmd = match parts[0] {
                    "nop" => CMD::Nop,
                    "jmp" => CMD::Jmp,
                    "acc" => CMD::Acc,
                    _ => CMD::Fuck,
                };

                program.push(Instruction {
                    cmd: cmd,
                    value: counter,
                })
            }
        }
    }

    let mut ip: usize = 0;
    let mut acc: i32 = 0;
    let mut visited_ips: HashSet<usize> = HashSet::new();
    loop {
        if visited_ips.contains(&ip) {
            println!("first duplicate ip: {}", ip);
            println!("accumulator is: {}", acc);
            break;
        }
        visited_ips.insert(ip);

        match program[ip].cmd {
            CMD::Fuck => panic!("fucked!"),
            CMD::Nop => ip += 1,
            CMD::Jmp => {
                if program[ip].value >= 0 {
                    ip += program[ip].value as usize;
                } else {
                    ip -= -program[ip].value as usize;
                }
            }
            CMD::Acc => {
                acc += program[ip].value;
                ip += 1;
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
