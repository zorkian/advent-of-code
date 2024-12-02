#!/bin/bash

DAY=$1
cp aoc/dayT.py aoc/day$DAY.py
touch inputs/day$DAY.test
touch inputs/day$DAY.data
