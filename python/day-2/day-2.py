#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import Counter


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    problems = []
    for ln in lines:
        tokens = ln.split(":")
        password = tokens[1].strip()
        tokens = tokens[0].split(" ")
        letter = tokens[1]
        min_occ, max_occ = tokens[0].split("-")
        min_occ, max_occ = int(min_occ), int(max_occ)
        problems.append((password, letter, min_occ, max_occ))
    return problems


def valid_passwd_part_one(pwd, letter, min_occ, max_occ):
    counter = Counter(pwd)
    occ = counter.get(letter, 0)
    return min_occ <= occ <= max_occ


def valid_passwd_part_two(pwd, letter, pos1, pos2):
    matches = int(pwd[pos1 - 1] == letter) + int(pwd[pos2 - 1] == letter)
    return matches == 1


if __name__ == '__main__':
    problems = load_input("day-2-input.txt")
    valid = 0
    for p in problems:
        if valid_passwd_part_one(*p):
            valid += 1
    print(valid)

    valid = 0
    for p in problems:
        if valid_passwd_part_two(*p):
            valid += 1
    print(valid)
