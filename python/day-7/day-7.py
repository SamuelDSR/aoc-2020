#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

contain_regex = re.compile(r'(([0-9]+) (\w+ (\w+))?) bags?[,\.]')
mainbag_regex = re.compile(r'(^\w+ (\w+)?) bags?')


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    bag_rules = {}
    for ln in lines:
        main_bag = mainbag_regex.findall(ln)[0][0]
        sub_bags = [(x[1], x[2]) for x in contain_regex.findall(ln)]
        bag_rules[main_bag] = sub_bags
    return bag_rules, len(lines)


def can_contain_target(bag, target, bag_rules):
    sub_bags = set([s[1] for s in bag_rules[bag]])
    if target in sub_bags:
        return True
    for sb in sub_bags:
        if can_contain_target(sb, target, bag_rules):
            return True
    return False


def part_1(bag_rules, target="shiny gold"):
    valid = 0
    for bag in bag_rules.keys():
        if can_contain_target(bag, target, bag_rules):
            valid += 1
    return valid


def capacity(bag, bag_rules):
    if len(bag_rules[bag]) == 0:
        return 1
    cap = 1
    for count, sb in bag_rules[bag]:
        cap += int(count) * capacity(sb, bag_rules)
    return cap


def part_2(bag_rules, target="shiny gold"):
    return capacity(target, bag_rules) - 1


if __name__ == '__main__':
    bag_rules, n = load_input("day-7-input.txt")
    print(part_1(bag_rules))
    print(part_2(bag_rules))
