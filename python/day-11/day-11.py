#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    return [list(ln.strip()) for ln in lines]


def adjacent(x, y, grid):
    occupied = 0
    for d in DIRS:
        nx, ny = x + d[0], y + d[1]
        if nx >= 0 and nx < len(grid) and ny >= 0 and ny < len(grid[0]):
            if grid[nx][ny] == '#':
                occupied += 1
    return occupied


def adjacent2(x, y, grid):
    occupied = 0
    for d in DIRS:
        nx, ny = x, y
        while True:
            nx, ny = nx + d[0], ny + d[1]
            if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[0]):
                break
            if grid[nx][ny] == '#':
                occupied += 1
                break
            elif grid[nx][ny] == 'L':
                break
            else:
                pass
    return occupied


def simulate(grid, target, adjacent_func):
    def step(grid):
        adjacent_grid = {}
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 'L' or grid[i][j] == '#':
                    adjacent_grid[(i, j)] = adjacent_func(i, j, grid)
        changes = 0
        for coord in adjacent_grid:
            i, j = coord
            if grid[i][j] == 'L' and adjacent_grid[coord] == 0:
                grid[i][j] = '#'
                changes += 1
            elif grid[i][j] == '#' and adjacent_grid[coord] >= target:
                grid[i][j] = 'L'
                changes += 1
            else:
                pass
        return changes

    while True:
        changes = step(grid)
        if changes == 0:
            break
    occupied = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                occupied += 1
    return occupied


if __name__ == '__main__':
    grid = load_input("day-11-input.txt")
    print(simulate(grid, 4, adjacent))
    grid = load_input("day-11-input.txt")
    print(simulate(grid, 5, adjacent2))
