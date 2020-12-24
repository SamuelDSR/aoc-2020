#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from collections import defaultdict
import re


def load_input():
    input_path = Path(__file__).parent / "input.txt"
    with input_path.open("r") as f:
        lines = f.readlines()
    pat = re.compile(r'(e|se|sw|w|nw|ne)')
    return [pat.findall(ln) for ln in lines]


MOVE_VECTORS = {
    "e": (3, 1),
    "se": (3, -1),
    "sw": (0, -2),
    "w": (-3, -1),
    "nw": (-3, 1),
    "ne": (0, 2)
}


def part_one(input):
    black_tiles = set()

    def _flip(moves):
        x, y = 0, 0
        for m in moves:
            x += MOVE_VECTORS[m][0]
            y += MOVE_VECTORS[m][1]
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))

    for moves in input:
        _flip(moves)
    answer = len(black_tiles)
    print("Answer to part one: {}".format(answer))
    return black_tiles


def part_two(black_tiles, days):
    def _adjacents(x, y):
        return [(x + m[0], y + m[1]) for m in MOVE_VECTORS.values()]

    for i in range(days):
        black_neighbors = defaultdict(int)
        for t in black_tiles:
            neighbors = _adjacents(*t)
            for n in neighbors:
                black_neighbors[n] += 1

        # black tile with zero black neighbors
        for t in list(black_tiles):
            if t not in black_neighbors:
                black_tiles.remove(t)

        for t, btn in black_neighbors.items():
            # black tile with > 2 black neighbors
            if btn > 2 and t in black_tiles:
                black_tiles.remove(t)
            # white tile with 2 black neighbors
            elif btn == 2 and t not in black_tiles:
                black_tiles.add(t)
            else:
                pass
    answer = len(black_tiles)
    print("Answer to part two: {}".format(answer))
    return black_tiles


if __name__ == '__main__':
    input = load_input()
    tiles_colors = part_one(input)
    part_two(tiles_colors, 100)
