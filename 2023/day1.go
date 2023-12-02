package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	p1 := flag.Bool("p1", false, "Run part1")
	p2 := flag.Bool("p2", false, "Run part2")
	test := flag.Bool("test", false, "Use test data")
	flag.Parse()

	if *p1 {
		part1(*test)
	} else if *p2 {
		part2(*test)
	} else {
		fmt.Println("Use -p1 or -p2")
	}
}

func part1(test bool) {
	file, err := os.Open("inputs/day1.input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	rv := int64(0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "")

		first, last := -1, -1
		for _, val := range line {
			intval, err := strconv.ParseInt(val, 10, 32)
			if err != nil {
				continue
			}
			if first == -1 {
				first = int(intval)
			} else {
				last = int(intval)
			}
		}
		if last == -1 {
			last = first
		}

		final, err := strconv.ParseInt(fmt.Sprintf("%d%d", first, last), 10, 32)
		if err != nil {
			panic(err)
		}

		rv += final
	}
	fmt.Println(rv)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

func part2(test bool) {
	refirst := regexp.MustCompile("^.*?([0-9]|one|two|three|four|five|six|seven|eight|nine)")
	relast := regexp.MustCompile("^.+([0-9]|one|two|three|four|five|six|seven|eight|nine).*?$")

	file, err := os.Open("inputs/day1.input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	rv := int64(0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		matches := refirst.FindStringSubmatch(line)
		if len(matches) == 0 {
			panic("broken")
		}

		first := valfrom(matches[1])
		last := first

		matches = relast.FindStringSubmatch(line)
		if len(matches) == 2 {
			last = valfrom(matches[1])
		}

		final, err := strconv.ParseInt(fmt.Sprintf("%d%d", first, last), 10, 32)
		if err != nil {
			panic(err)
		}

		rv += final
	}
	fmt.Println(rv)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

func valfrom(inp string) int {
	switch inp {
	case "one":
		return 1
	case "two":
		return 2
	case "three":
		return 3
	case "four":
		return 4
	case "five":
		return 5
	case "six":
		return 6
	case "seven":
		return 7
	case "eight":
		return 8
	case "nine":
		return 9
	default:
		tv, err := strconv.ParseInt(inp, 10, 32)
		if err != nil {
			panic(err)
		}
		return int(tv)
	}
}
