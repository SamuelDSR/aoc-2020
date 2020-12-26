#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path


def load_input():
    input_path = Path(__file__).parent / "input.txt"
    with Path(input_path).open('r') as f:
        lines = f.readlines()
    arrival_time = int(lines[0])
    bus_ids_offsets = []
    for i, bus_id in enumerate(lines[1].split(",")):
        if bus_id != 'x':
            bus_ids_offsets.append((i, int(bus_id)))
    return arrival_time, bus_ids_offsets


def part_1(arrival_time, bus_ids_offsets):
    waits = [(bus_id, bus_id - arrival_time % bus_id)
             for _, bus_id in bus_ids_offsets]
    bus_id, least_wait = min(waits, key=lambda x: x[1])
    return bus_id * least_wait


def inverse_mod(product, divisor):
    k = 0
    while True:
        k += 1
        if product * k % divisor == 1:
            break
    return product * k


def prod(numbers):
    p = 1
    for n in numbers:
        p *= n
    return p


def part_2(bus_ids_offsets):
    """The problem of part_2 can be solved using the 
    [chinese remainder theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem)
    """
    first_element = bus_ids_offsets[0][1]
    bus_ids_offsets = bus_ids_offsets[1:]

    product = prod([bid[1] for bid in bus_ids_offsets])
    inverses = []
    for offset, bus_id in bus_ids_offsets:
        if offset > bus_id:
            offset = bus_id - offset % bus_id
        else:
            offset = bus_id - offset
        inverses.append((offset, inverse_mod(product // bus_id, bus_id)))
    sum_inverses = sum([i[0] * i[1] for i in inverses])
    # the general solutions that satisify the offset conditions would be: sum_inverses+ k*product,
    # where k is integer (could be negative), now we need to find the the smallest k which makes
    # (sum_inverses + k*product) is a multiple of the first element!
    k = -sum_inverses // product
    while True:
        candidate = sum_inverses + k * product
        if candidate % first_element == 0:
            return candidate
        k += 1
    return None


if __name__ == '__main__':
    arrival_time, bus_ids_offsets = load_input()
    print(part_1(arrival_time, bus_ids_offsets))
    assert part_2([(0, 17), (2, 13), (3, 19)]) == 3417
    assert part_2([(0, 67), (1, 7), (2, 59), (3, 61)]) == 754018
    assert part_2([(0, 67), (2, 7), (3, 59), (4, 61)]) == 779210
    print(part_2(bus_ids_offsets))
