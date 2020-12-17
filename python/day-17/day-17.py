#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import partial
from itertools import product
from pathlib import Path


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    actives = set()
    for i in range(len(lines)):
        ln = lines[i]
        for j in range(len(ln)):
            if ln[j] == '#':
                actives.add((i, j))
    return actives


def adjacent(coord, deltas):
    adjs = []
    for delta in deltas:
        new_coord = tuple(a + b for a, b in zip(coord, delta))
        if new_coord != coord:
            adjs.append(new_coord)
    return adjs


def expand(coord, dims):
    if len(coord) < dims:
        return tuple(list(coord) + [0] * (dims - len(coord)))
    return coord


def step(actives, adj_func):
    neighbors = defaultdict(int)
    for s in actives:
        for adj in adj_func(s):
            neighbors[adj] += 1
    new_actives = set()
    for n in neighbors:
        if n in actives:
            if neighbors[n] == 2 or neighbors[n] == 3:
                new_actives.add(n)
        else:
            if neighbors[n] == 3:
                new_actives.add(n)
    return new_actives


def simulate(initial_state, adj_func, n):
    actives = initial_state
    for i in range(n):
        actives = step(actives, adj_func)
    return len(actives)


if __name__ == '__main__':
    initial_state = load_input("day-17-input.txt")
    print(initial_state)
    print(
        simulate([expand(s, 3) for s in initial_state],
                 partial(adjacent, deltas=list(product(*[(1, 0, -1)] * 3))),
                 6))
    print(
        simulate([expand(s, 4) for s in initial_state],
                 partial(adjacent, deltas=list(product(*[(1, 0, -1)] * 4))),
                 6))
