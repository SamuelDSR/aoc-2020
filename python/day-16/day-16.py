#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import defaultdict


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()

    def _parse_rules(ln):
        field, ranges = ln.split(":")
        ranges = [[int(x) for x in r.split("-")] for r in ranges.split(" or ")]
        return field, ranges

    your_ticket_ln = lines.index("your ticket:\n")
    nearby_ticket_ln = lines.index("nearby tickets:\n")
    rules = {}
    for ln in lines[:your_ticket_ln - 1]:
        field, ranges = _parse_rules(ln)
        rules[field] = ranges
    ticket = [int(x) for x in lines[your_ticket_ln + 1].split(",")]
    nearby_tickets = [[int(x) for x in ln.split(",")]
                      for ln in lines[nearby_ticket_ln + 1:]]
    return rules, ticket, nearby_tickets


def part_1(rules, nearby_tickets):
    invalids, invalid_ticket_idx = [], set()
    all_ranges = []
    for r in rules.values():
        all_ranges += r
    for i, t in enumerate(nearby_tickets):
        for v in t:
            if not any(minv <= v <= maxv for minv, maxv in all_ranges):
                invalids.append(v)
                invalid_ticket_idx.add(i)
    return sum(invalids), invalid_ticket_idx


def part_2(ticket, rules, nearby_tickets):
    def _candidate_fields(numbers, rules):
        """Return the fields which are valid for all given numbers
        """
        valid_fields = []
        for field, ranges in rules.items():
            if all(
                    any(minv <= n <= maxv for minv, maxv in ranges)
                    for n in numbers):
                valid_fields.append(field)
        return valid_fields

    # field => possible indexes
    mappings = defaultdict(set)
    for i in range(len(rules)):
        numbers = [t[i] for t in nearby_tickets]
        for f in _candidate_fields(numbers, rules):
            mappings[f].add(i)

    determined_set = []
    while len(mappings) > 0:
        for field, indexes in mappings.items():
            if len(indexes) == 1:
                determined_set.append((field, list(indexes)[0]))
        for field, idx in determined_set:
            if field in mappings:
                del mappings[field]
            for field, indexes in mappings.items():
                if idx in indexes:
                    indexes.remove(idx)
    determined_mapping = dict((t[1], t[0]) for t in determined_set)
    product = 1
    for i, v in enumerate(ticket):
        if determined_mapping[i].startswith("departure"):
            product *= v
    return product


if __name__ == '__main__':
    rules, ticket, nearby_tickets = load_input("day-16-input.txt")
    invalid_sum, invalid_ticket_idx = part_1(rules, nearby_tickets)
    print(invalid_sum, invalid_ticket_idx)
    valid_nearby_tickets = [
        nearby_tickets[i] for i in range(len(nearby_tickets))
        if i not in invalid_ticket_idx
    ]
    print(part_2(ticket, rules, valid_nearby_tickets))
