#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import Counter


def load_input():
    input_path = Path(__file__).parent / "input.txt"
    with Path(input_path).open('r') as f:
        lines = f.readlines()
    return [int(l.strip()) for l in lines]


def part_1(numbers):
    numbers = sorted(numbers)
    diff = Counter([y - x for x, y in zip(numbers[0:-1], numbers[1:])])
    print(diff)
    return (diff[3] + 1) * (diff[1] + 1)


def part_2(numbers):
    """
    Dynamic programming: 
    in a reverse order,  solution(n): numbers of distinct valid ways that n is ending
    solution(n) = solution(n+1) + solution(n+2) + solution(n+3) if n+1/n+2/n+3 are in numbers
    """
    numbers = sorted(numbers, reverse=True)
    max_n = max(numbers)
    solution = {}
    solution[numbers[0]] = 1

    def part_2_util(n):
        if n > max_n:
            return 0
        if n in solution:
            return solution[n]
        else:
            c1 = part_2_util(n + 1) if (n + 1) in numbers else 0
            c2 = part_2_util(n + 2) if (n + 2) in numbers else 0
            c3 = part_2_util(n + 3) if (n + 3) in numbers else 0
            count = c1 + c2 + c3
            solution[n] = count
            return count

    for n in numbers[1:]:
        part_2_util(n)
    return solution.get(1, 0) + solution.get(2, 0) + solution.get(3, 0)


if __name__ == '__main__':
    numbers = load_input()
    print(part_1(numbers))
    print(part_2([1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]))
    print(part_2(numbers))
