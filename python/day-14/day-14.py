#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import product


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    instructions = []
    for ln in lines:
        op, number = ln.split("=")
        if op.startswith("mask"):
            instructions.append((op.strip(), number.strip()))
        else:
            instructions.append((int(op.strip()[4:-1]), int(number)))
    return instructions


def mask(number, mask_string, memory_width):
    bins = list(bin(number)[2:])
    if len(bins) < memory_width:
        bins = ['0' for i in range(memory_width - len(bins))] + bins
    for i, m in enumerate(mask_string):
        if m == '1' or m == '0':
            bins[i] = m
    return int("".join(bins), 2)


def mask2(number, mask_string, memory_width):
    bins = list(bin(number)[2:])
    if len(bins) < memory_width:
        bins = ['0' for i in range(memory_width - len(bins))] + bins
    floating_bits = []
    for i, m in enumerate(mask_string):
        if m == '1':
            bins[i] = '1'
        elif m == 'X':
            floating_bits.append(i)
        else:
            pass
    numbers = []
    for comb in product(*[['0', '1']] * len(floating_bits)):
        for idx, addr in enumerate(floating_bits):
            bins[addr] = str(comb[idx])
        numbers.append(int("".join(bins), 2))
    return numbers


def part_1(instructions):
    memory = {}
    current_mask = None
    for ins in instructions:
        if ins[0] == 'mask':
            current_mask = ins[1]
        else:
            memory[ins[0]] = mask(ins[1], current_mask, 36)
    return sum(memory.values())


def part_2(instructions):
    memory = {}
    current_mask = None
    for ins in instructions:
        if ins[0] == 'mask':
            current_mask = ins[1]
        else:
            for addr in mask2(ins[0], current_mask, 36):
                memory[addr] = ins[1]
    return sum(memory.values())


if __name__ == '__main__':
    instructions = load_input("day-14-input.txt")
    assert mask(11, 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 36) == 73
    assert mask(101, 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 36) == 101
    print(part_1(instructions))
    assert mask2(42, '000000000000000000000000000000X1001X', 36) == [26, 27, 58, 59]
    assert mask2(26, '00000000000000000000000000000000X0XX', 36) == [16, 17, 18, 19, 24, 25, 26, 27]
    print(part_2(instructions))
    
