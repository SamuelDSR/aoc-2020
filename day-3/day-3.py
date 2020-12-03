#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    return np.array([list(ln.strip()) for ln in lines])


def traverse_grid(grid, rows, cols):
    cur_row, cur_col = 0, 0
    trees = 0
    while cur_row < grid.shape[0]:
        if grid[cur_row][cur_col % grid.shape[1]] == "#":
            trees += 1
        cur_row += rows
        cur_col += cols
    return trees

if __name__ == '__main__':
    grid = load_input("day-3-input.txt")
    answer1 = traverse_grid(grid, 1, 3)
    print(answer1)

    rows = [1, 1, 1, 1, 2]
    cols = [1, 3, 5, 7, 1]
    answer2 = 1
    for x, y in zip(rows, cols):
        answer2*=traverse_grid(grid, x, y)
    print(answer2)
