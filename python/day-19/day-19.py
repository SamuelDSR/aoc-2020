#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import defaultdict
from itertools import combinations, product


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


def is_valid(string, rules, basic_rule=0, known_rules=None):
    def valid_for_rule(substring, rule, memory):
        key = (substring, rule)
        if key in memory:
            return memory[key]
        elif known_rules is not None and rule in known_rules:
            return known_rules[rule](substring)
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

    result = valid_for_rule(string, basic_rule, {})
    return result


def part_1(rules, inputs, basic_rule=0):
    return sum(is_valid(string, rules, basic_rule) for string in inputs)


def possible_strings(r, rules):
    if isinstance(r, str):
        return [r]
    ways = []
    for subrules in rules[r]:
        for prod in product(*[possible_strings(xr, rules) for xr in subrules]):
            base = []
            for p in prod:
                base += p
            ways.append("".join(base))
    return ways


def part_2(rules, inputs):
    ways_of_42 = possible_strings(42, rules)
    assert part_1(rules, ways_of_42, basic_rule=42) == len(ways_of_42)
    ways_of_31 = possible_strings(31, rules)
    assert part_1(rules, ways_of_31, basic_rule=31) == len(ways_of_31)

    # luckily, all ways of 42/31 has the same length of 8
    def valid_for_42(substring):
        return substring in ways_of_42

    def valid_for_31(substring):
        return substring in ways_of_31

    def valid_for_8(substring):
        if len(substring) % 8 != 0:
            return False
        if len(substring) == 8:
            if substring in ways_of_42:
                return True
            else:
                return False
        return valid_for_8(substring[:8]) and valid_for_8(substring[8:])

    def valid_for_11(substring):
        if len(substring) % 16 != 0:
            return False
        if len(substring) == 16:
            if substring[:8] in ways_of_42 and substring[8:] in ways_of_31:
                return True
            else:
                return False
        return valid_for_11(substring[:8] + substring[-8:]) and valid_for_11(
            substring[8:-8])

    known_rules = {
        42: valid_for_42,
        31: valid_for_31,
        8: valid_for_8,
        11: valid_for_11
    }
    return sum(
        is_valid(string, rules, 0, known_rules) for string in inputs)


if __name__ == '__main__':
    assert len(string_partitions("samuel", 3)) == 10
    assert len(string_partitions("samuel", 1)) == 1
    assert len(string_partitions("samuel", 7)) == 0

    rules, inputs = load_input("day-19-input.txt")
    print(part_1(rules, inputs))
    print(part_2(rules, inputs))
