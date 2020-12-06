#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

def load_input(path):
    with Path(path).open('r') as f:
        lines = f.read()
    return lines.split("\n\n")

def part_1(group_answers):
    return sum([
        len(set(x.replace("\n", "")))
        for x in group_answers
    ])

def part_2(group_answers):
    return sum([
        len(set.intersection(*(set(a) for a in answers.strip().split("\n"))))
        for answers in group_answers
    ])

if __name__ == '__main__':
    group_answers = load_input("day-6-input.txt")
    print(part_1(group_answers))
    print(part_2(group_answers))
