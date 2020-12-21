#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from functools import reduce
from collections import defaultdict


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    foods = {}
    for food_idx, ln in enumerate(lines):
        separator = ln.strip().index("(")
        ingredients = ln[:separator].strip().split(" ")
        allergens = [
            a.strip() for a in ln[separator:].strip()[9:-1].split(",")
        ]
        foods[food_idx] = [set(ingredients), set(allergens)]
    return foods


def part_1(foods):
    # get all allergens
    allergens = reduce(lambda a, b: a | b, map(lambda f: f[1], foods.values()), set([]))

    allergen_food_mapping = defaultdict(set)
    for allergen in allergens:
        for food_idx, receipe in foods.items():
            if allergen in receipe[1]:
                allergen_food_mapping[allergen].add(food_idx)
    #  print(allergen_food_mapping)
    allergen_ingredient_mapping = {}
    for allergen in allergen_food_mapping:
        possible_ingredients = [foods[idx][0] for idx in allergen_food_mapping[allergen]]
        possible_ingredients = reduce(lambda a, b: a & b,
                                      possible_ingredients[1:],
                                      possible_ingredients[0])
        allergen_ingredient_mapping[allergen] = possible_ingredients

    final_mapping = {}
    while len(allergen_ingredient_mapping) > 0:
        for allergen in allergens:
            if len(allergen_ingredient_mapping.get(allergen, [])) == 1:
                ingredient = allergen_ingredient_mapping[allergen].pop()
                final_mapping[allergen] = ingredient
                del allergen_ingredient_mapping[allergen]
                for ingredient_set in allergen_ingredient_mapping.values():
                    if ingredient in ingredient_set:
                        ingredient_set.remove(ingredient)
    assert len(final_mapping) == len(allergens), "some allergens not determined"
    known_ingredients = set(final_mapping.values())
    count = 0
    for ingredients, _ in foods.values():
        count += len(ingredients - known_ingredients)
    print("Answer to part 1: {}".format(count))
    return final_mapping


def part_2(final_mapping):
    # sort ingredients by their allergens alphabetically
    mappings = [x for x in final_mapping.items()]
    ingredients = [x[1] for x in sorted(mappings, key=lambda x: x[0])]
    print("Answer to part 2: {}".format(",".join(ingredients)))


if __name__ == '__main__':
    foods = load_input("day-21-input.txt")
    final_mapping = part_1(foods)
    part_2(final_mapping)
