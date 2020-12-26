#!/usr/bin/env python
# -*- coding: utf-8 -*-

def rambuctious_recitation(numbers, ending):
    occurence = {}
    for i, n in enumerate(numbers[:-1]):
        occurence[n] = i
    last_i = i + 1
    last_number = numbers[last_i]
    while True:
        if last_i + 1 == ending:
            break
        if last_number in occurence:
            to_add = last_i - occurence[last_number]
            occurence[last_number] = last_i
            last_i += 1
        else:
            occurence[last_number] = last_i
            to_add = 0
            last_i += 1
        last_number = to_add
    return last_number


if __name__ == '__main__':
    assert rambuctious_recitation([1, 3, 2], 2020) == 1
    assert rambuctious_recitation([2, 1, 3], 2020) == 10
    print(rambuctious_recitation([19, 20, 14, 0, 9, 1], 2020))

    assert rambuctious_recitation([2, 1, 3], 30000000) == 3544142
    print(rambuctious_recitation([19, 20, 14, 0, 9, 1], 30000000))
