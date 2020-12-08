#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    instructions = []
    for ln in lines:
        t = ln.strip().split(" ")
        instructions.append([t[0], int(t[1])])
    return instructions


def run(instructions):
    """
    return accumulator and the reason the program terminates
    0: going to a repeat loop
    1: terminates normally
    """
    acc, index = 0, 0
    seens = set()
    while True:
        if index in seens:
            return acc, 0
        if index >= len(instructions) or index < 0:
            return acc, 1
        seens.add(index)
        opcode, number = instructions[index]
        if opcode == "acc":
            acc += number
            index += 1
        elif opcode == "jmp":
            index += number
        elif opcode == "nop":
            index += 1
        else:
            pass
    return acc


def part_1(instructions):
    answer, reason = run(instructions)
    return answer


def part_2(instructions):
    """
    brutal force search for changing one jump to nop or nop to jump,
    not a good approach
    """
    for i in range(len(instructions)):
        opcode, number = instructions[i]
        if opcode == "jmp":
            instructions[i][0] = "nop"
        elif opcode == "nop":
            instructions[i][0] = "jmp"
        else:
            pass
        acc, reason = run(instructions)
        if reason == 1:
            return acc
        instructions[i][0] = opcode
    return None


if __name__ == '__main__':
    instructions = load_input("day-8-input.txt")
    print(part_1(instructions))
    print(part_2(instructions))
