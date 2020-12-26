#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import deque, defaultdict


def load_input():
    input_path = Path(__file__).parent / "input.txt"
    with Path(input_path).open('r') as f:
        lines = f.readlines()
    return [int(l.strip()) for l in lines]


def part_1(numbers, premable_count):
    two_sums = defaultdict(int)
    premable_set = deque([])
    for i, n in enumerate(numbers):
        if i < premable_count:
            for x in premable_set:
                two_sums[x + n] += 1
            premable_set.append(n)
        else:
            if n not in two_sums:
                return n
            else:
                to_remove = premable_set.popleft()
                for x in premable_set:
                    s1 = to_remove + x
                    s2 = n + x
                    two_sums[s1] -= 1
                    if two_sums[s1] <= 0:
                        del two_sums[s1]
                    two_sums[s2] += 1
                premable_set.append(n)
    return None


def part_2(numbers, target):
    """Brutal force
    """
    sums = defaultdict(set)
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            sums[sum(numbers[i:j + 1])].add((i, j))
    lower, upper = list(sums[target])[0]
    return min(numbers[lower:upper + 1]) + max(numbers[lower:upper + 1])


if __name__ == '__main__':
    numbers = load_input()
    target = part_1(numbers, 25)
    print(part_2(numbers, target))
