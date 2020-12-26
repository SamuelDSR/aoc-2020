#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

def seat_to_int(seat_code):
    seat_row = int(seat_code[:7].replace("F", "0").replace("B", "1"), 2)
    seat_col = int(seat_code[7:].replace("R", "1").replace("L", "0"), 2)
    return seat_row*8 + seat_col

def load_input():
    input_path = Path(__file__).parent / "input.txt"
    with Path(input_path).open('r') as f:
        lines = f.readlines()
    seat_codes = [
        seat_to_int(ln.strip()) for ln in lines
    ]
    return seat_codes

def part_1(seat_codes):
    return max(seat_codes)

def part_2(seat_codes):
    lower = min(seat_codes)
    upper = max(seat_codes)
    return list((set(range(lower, upper+1)) - set(seat_codes)))[0]

if __name__ == '__main__':
    seat_codes = load_input()
    print(part_1(seat_codes))
    print(part_2(seat_codes))

