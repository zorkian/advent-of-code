use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, PartialEq)]
enum TermType {
    Integer,
    Operator,
    Expression,
}

#[derive(Debug, PartialEq)]
enum Operator {
    None,
    Addition,
    Multiplication,
}

#[derive(Debug)]
struct Term {
    term_type: TermType,
    operator: Operator,
    value: u64,
    expression: Expression,
}

type Expression = Vec<Term>;

fn parse_expression(inp: Vec<&str>) -> Expression {
    let mut exprs: Vec<Expression> = Vec::new();

    // Start a new empty expression
    exprs.push(Vec::new());

    for i in 0..inp.len() {
        //dbg!(&exprs);
        let bytes = inp[i].as_bytes();
        let mut exprct = exprs.len();
        let mut offset: usize = 0;
        let mut inset: usize = bytes.len();
        let mut unwraps: usize = 0;

        // First, see if we're ending an expression
        // 1 + (3 + (2 * 5))
        //  Term(1)
        //  Term(+)
        //  Term(Expr: Term(3) Term(+) ...
        //  Term(Expr: Term(2) Term(*) ...
        while bytes[inset - 1] == 41 {
            // )
            inset -= 1;
            unwraps += 1;
            continue;
        }

        // We're not ending, so see if we're starting one (or several)
        while bytes[offset] == 40 {
            // (
            exprs.push(Vec::new());
            exprct += 1;
            offset += 1;
            continue;
        }

        // Nope, this is just a term, get the most recent expression
        // which is the open one and add to it
        let expr = exprs.get_mut(exprct - 1).unwrap();
        if bytes[offset] == 43 {
            // +
            expr.push(Term {
                term_type: TermType::Operator,
                value: 0,
                expression: Vec::new(),
                operator: Operator::Addition,
            });
        } else if bytes[offset] == 42 {
            // *
            expr.push(Term {
                term_type: TermType::Operator,
                value: 0,
                expression: Vec::new(),
                operator: Operator::Multiplication,
            });
        } else {
            // Must be a number, per the spec
            expr.push(Term {
                term_type: TermType::Integer,
                value: String::from_utf8(bytes[offset..inset].to_vec())
                    .unwrap()
                    .parse::<u64>()
                    .unwrap(),
                expression: Vec::new(),
                operator: Operator::None,
            });
        }

        // Now perform unwrapping passes
        for _i in 0..unwraps {
            let cur_expr = exprs.remove(exprct - 1);
            exprct -= 1;
            let expr = exprs.get_mut(exprct - 1).unwrap();
            expr.push(Term {
                term_type: TermType::Expression,
                value: 0,
                expression: cur_expr,
                operator: Operator::None,
            });
        }
    }

    // This probably holds on to the containing vec?
    //dbg!(&exprs);
    return exprs.remove(0);
}

fn run_expression(exp: Expression) -> u64 {
    let mut value;
    let mut temp_expr: Expression = Vec::new();

    // First pass, filter for addition and perform it immediately,
    // inserting into temp_expr
    for term in exp {
        // If operator, just push it
        if term.term_type == TermType::Operator {
            println!("pushing operator {:?}", term);
            temp_expr.push(term);
            continue;
        }

        // Expression or int, downconvrt to int
        let int_term = match term.term_type {
            TermType::Expression => {
                value = run_expression(term.expression);
                Term {
                    term_type: TermType::Integer,
                    value: value,
                    expression: Vec::new(),
                    operator: Operator::None,
                }
            }
            TermType::Integer => term,
            _ => panic!("impossible"),
        };
        println!("considering int {:?}", int_term);

        // If there aren't enough terms or previous wasn't addition, skip
        let len = temp_expr.len();
        if len < 3 || temp_expr[len - 1].operator != Operator::Addition {
            temp_expr.push(int_term);
            continue;
        }

        // Perform in-place addition
        dbg!(&temp_expr);
        value = int_term.value + temp_expr[len - 2].value;
        dbg!(value);
        temp_expr.remove(len - 1);
        temp_expr[len - 2].value = value;
        dbg!(&temp_expr);
    }

    return run_expression_all(temp_expr);
}

fn run_expression_all(exp: Expression) -> u64 {
    let mut value = 0;
    let mut operator = Operator::None;

    for term in exp {
        match term.term_type {
            TermType::Operator => operator = term.operator,
            TermType::Integer => match operator {
                Operator::None => value = term.value,
                Operator::Addition => value += term.value,
                Operator::Multiplication => value *= term.value,
            },
            TermType::Expression => match operator {
                Operator::None => value = run_expression(term.expression),
                Operator::Addition => value += run_expression(term.expression),
                Operator::Multiplication => value *= run_expression(term.expression),
            },
        }
    }

    return value;
}

fn main() {
    let mut valid_ct = 0;

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(lin) = line {
                // 1-3 c: cctdcvcdqc
                let parts: Vec<&str> = lin.split(" ").collect();

                let expr = parse_expression(parts);
                valid_ct += run_expression(expr);
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
