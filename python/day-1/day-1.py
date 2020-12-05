#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from collections import Counter

def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    return lines


def prod_of_two(numbers_counter, target):
    for n in numbers_counter:
        numbers_counter[n] -= 1
        remain = target - n
        if numbers_counter.get(remain, 0) > 0:
            return n*remain
        else:
            numbers_counter[n] += 1
    return None


def prod_of_three(numbers_counter, target):
    for n in numbers:
        remain_target = target - n
        numbers_counter[n] -= 1
        ret = prod_of_two(numbers_counter, remain_target)
        if ret is not None:
            return ret*n
        numbers_counter[n] += 1


if __name__ == '__main__':
    numbers = Counter([
        int(n) for n in load_input('day-1-input.txt')
    ])
    answer = prod_of_two(numbers, 2020)
    print(answer)

    answer2 = prod_of_three(numbers, 2020)
    print(answer2)
