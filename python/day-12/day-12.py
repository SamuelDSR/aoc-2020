#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    return [(ln[0], int(ln[1:])) for ln in lines]


def rot(direction, action, degree):
    dx, dy = direction
    for i in range(degree // 90):
        if action == 'L':
            dx, dy = -dy, dx
        else:
            dx, dy = dy, -dx
    return dx, dy


def step(instruction, direction, pos):
    """
    x => axis west-east
    y => axis north-south
    direction:
        facing east: (1, 0)
        facing north: (0, 1)
        facing west: (-1, 0)
        facing south: (0, -1)
    """
    action, delta = instruction
    dx, dy = direction
    x, y = pos
    if action == 'N':
        y += delta
    elif action == 'S':
        y -= delta
    elif action == 'E':
        x += delta
    elif action == 'W':
        x -= delta
    elif action == 'L' or action == 'R':
        dx, dy = rot((dx, dy), action, delta)
    else:
        x, y = x + delta * dx, y + delta * dy
    return (dx, dy), (x, y)


def step2(instruction, direction, pos):
    action, delta = instruction
    dx, dy = direction
    x, y = pos
    if action == 'N':
        dy += delta
    elif action == 'S':
        dy -= delta
    elif action == 'E':
        dx += delta
    elif action == 'W':
        dx -= delta
    elif action == 'L' or action == 'R':
        dx, dy = rot((dx, dy), action, delta)
    else:
        x, y = x + delta * dx, y + delta * dy
    return (dx, dy), (x, y)


def move(instruction, step_func, direction=(1, 0), pos=(0, 0)):
    for instruction in instructions:
        direction, pos = step_func(instruction, direction, pos)
    return abs(pos[0]) + abs(pos[1])


if __name__ == '__main__':
    print(rot((1, 0), 'L', 270))
    print(rot((1, 0), 'R', 180))
    instructions = load_input("day-12-input.txt")
    print(move(instructions, step))
    print(move(instructions, step2, direction=(10, 1), pos=(0, 0)))
