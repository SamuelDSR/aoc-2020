#!/usr/bin/env python
# -*- coding: utf-8 -*-


def cal_public_key(subject_number, target_numbers, max_loop=None):
    to_search, loop_sizes = set(target_numbers), {}
    i, value = 0, 1
    while (max_loop is None) or i <= max_loop:
        i += 1
        value *= subject_number
        value = value % 20201227
        if value in to_search:
            to_search.remove(value)
            loop_sizes[value] = i
        if len(to_search) == 0:
            break
    return loop_sizes, value


if __name__ == '__main__':
    #  card_key, door_key = 5764801, 17807724
    card_key, door_key = 6929599, 2448427
    loop_sizes, _ = cal_public_key(7, [card_key, door_key])
    card_loop, door_loop = loop_sizes[card_key], loop_sizes[door_key]
    _, answer1 = cal_public_key(card_key, [-1], door_loop - 1)
    _, answer2 = cal_public_key(door_key, [-1], card_loop - 1)
    assert answer1 == answer2
    print("Answer is: {}".format(answer1))
