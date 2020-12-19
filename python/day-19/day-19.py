#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import defaultdict
from itertools import combinations


def load_input(path):
    with Path(path).open("r") as f:
        lines = f.readlines()
    idx = lines.index("\n")
    rules = defaultdict(list)
    for ln in lines[:idx]:
        parent, children = ln.split(":")
        for child in children.strip().split("|"):
            if '"' not in child:
                rules[int(parent)].append(
                    [int(c) for c in child.strip().split(" ")])
            else:
                rules[int(parent)] = child.strip().replace('"', "")
    inputs = [ln.strip() for ln in lines[idx + 1:]]
    return rules, inputs


def string_partitions(string, n):
    """Return all possible ways that divide string into <n> partitions
    Note: all partitions must have a least one character
    """
    partitions = []
    for indexes in combinations(range(len(string) - 1), n - 1):
        substrings, start = [], 0
        for i in indexes:
            substrings.append(string[start:i + 1])
            start = i + 1
        substrings.append(string[start:])
        partitions.append(substrings)
    return partitions


def is_valid(string, rules):
    def valid_for_rule(substring, rule, memory):
        key = (substring, rule)
        if key in memory:
            return memory[key]
        # basic case: reach a basic rule
        elif isinstance(rules[rule], str):
            if rules[rule] == substring:
                memory[key] = True
                ret = True
            else:
                memory[key] = False
                ret = False
        else:
            if any(
                    all(
                        valid_for_rule(p, r, memory)
                        for p, r in zip(partition, subrules))
                    for subrules in rules[rule] for partition in
                    string_partitions(substring, len(subrules))):
                memory[key] = True
                ret = True
            else:
                memory[key] = False
                ret = False
        return ret

    result = valid_for_rule(string, 0, {})
    return result


def part_1(rules, inputs):
    return sum(is_valid(string, rules) for string in inputs)


def part_2(rules, inputs):
    def part2_is_valid(string, rules, max_i, max_j):
        for i in range(1, max_i):
            for j in range(1, max_j):
                rules[8] = [[42] * i]
                rules[11] = [[42] * j + [31] * j]
                if is_valid(string, rules):
                    print("{} is valid for 8:{}, 11:{}".format(string, i, j))
                    return True
                else:
                    print("{} is invalid for 8:{}, 11:{}".format(string, i, j))
        return False

    valid_cnt = 0
    for string in inputs:
        if part2_is_valid(string, rules, 10, 3):
            valid_cnt += 1
    return valid_cnt


if __name__ == '__main__':
    assert len(string_partitions("samuel", 3)) == 10
    assert len(string_partitions("samuel", 1)) == 1
    assert len(string_partitions("samuel", 7)) == 0

    rules, inputs = load_input("day-19-input.txt")
    print(part_1(rules, inputs))
    print(part_2(rules, inputs))
