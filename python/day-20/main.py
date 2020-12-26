#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import reduce
from operator import mul
from pathlib import Path


def compose(*funcs):
    def inner(arg):
        for f in reversed(funcs):
            arg = f(arg)
        return arg

    return inner


def _rot90(matrix):
    """Rotate a python matrix (list of list) without numpy
    https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-matrix-in-python
    """
    return list(zip(*matrix[::-1]))


def flip_horizontal(matrix):
    return [arr[::-1] for arr in matrix]


def flip_vertical(matrix):
    return matrix[::-1]


class Tile:
    def __init__(self, tile_id, tile_array):
        self.tile_id = tile_id
        self.tile_array = tile_array

    @classmethod
    def load_tiles_from_file(cls, path):
        input_path = Path(__file__).parent / "input.txt"
        with Path(input_path).open('r') as f:
            content = f.read().strip()
        return [
            Tile(int(tokens[0][5:-1]), tokens[1:])
            for tokens in map(lambda x: x.split("\n"), content.split("\n\n"))
        ]

    def transforms(self):
        all_transforms = {
            "rot90": _rot90,
            "rot180": compose(_rot90, _rot90),
            "rot270": compose(_rot90, _rot90, _rot90),
            "rot360": compose(_rot90, _rot90, _rot90, _rot90),
            "flip_h": flip_horizontal,
            "flip_v": flip_vertical,
            "rot90_filp_h": compose(_rot90, flip_horizontal),
            "rot90_flip_v": compose(_rot90, flip_vertical)
        }
        for key, transform_func in all_transforms.items():
            yield Tile(-1, transform_func(self.tile_array))

    def all_possible_boarders(self):
        boarders = set()
        for tile in self.transforms():
            boarders.update(tile.get_boarders())
        return boarders

    def get_boarders(self):
        up = "".join(self.tile_array[0])
        down = "".join(self.tile_array[-1])
        left = "".join([row[0] for row in self.tile_array])
        right = "".join([row[-1] for row in self.tile_array])
        return [up, down, left, right]

    def __hash__(self):
        return self.tile_id

    def __str__(self):
        return "\n".join(["".join(row) for row in self.tile_array])

    def get_opposite_boarder(self, b):
        """Given boarder b, return the opposite boarder
        e.g., given left boarder, return the right boarder
        """
        boarders = self.get_boarders()
        idx = boarders.index(b)
        if idx == 0:  # up
            return boarders[1]
        elif idx == 1:  # down
            return boarders[0]
        elif idx == 2:  # left
            return boarders[3]
        elif idx == 3:  # right
            return boarders[2]
        else:
            raise Exception("Something is wrong about opposite boarders")

    def arange_tile_to_match_boarders(self, boarder, idx):
        """Transform the tile to be able to match the given boarder and corresponding positions
        Return true if this possible, false otherwise.
        idx: 0 => Up, 1 => Down, 2 => Left, 3 => Right
        """
        for tile in self.transforms():
            tile_boarders = tile.get_boarders()
            if tile_boarders[idx] == boarder:
                self.tile_array = tile.tile_array
                return
        raise Exception("Something is wrongin arange boarders")

    def remove_boarders(self):
        return [arr[1:-1] for arr in self.tile_array[1:-1]]


def part_1(tiles):
    """The tiles at the four corner should have two boarders
    that doesn't appear in other tiles
    """
    print("Number of tiles: {}".format(len(tiles)))  # 144 = 12x12 tiles
    boarder_to_tile_mapping = defaultdict(set)
    for tile in tiles:
        for b in tile.all_possible_boarders():
            boarder_to_tile_mapping[b].add(tile)

    # Image boarders should be those that appears in only one tile
    # 96 found !, but removing the reversed versions,
    # we find all 92/2=48 image boarders for the 12x12 tile image
    image_boarders = [
        b for b in boarder_to_tile_mapping
        if len(boarder_to_tile_mapping[b]) == 1
    ]
    # remove the reversed version
    unique_image_boarders = set()
    for b in image_boarders:
        if b not in unique_image_boarders and \
                b[::-1] not in unique_image_boarders:
            unique_image_boarders.add(b)
    # 48, confirmed!
    print("Number of unique boards: {}".format(len(unique_image_boarders)))

    # the four corner tiles should be thoses that have two image boarders
    tile_to_image_boarder_mapping = defaultdict(set)
    for b in unique_image_boarders:
        for tile in boarder_to_tile_mapping[b]:
            tile_to_image_boarder_mapping[tile].add(b)
    corner_tiles = [
        tile for tile in tile_to_image_boarder_mapping
        if len(tile_to_image_boarder_mapping[tile]) == 2
    ]
    print("Answer to part 1: {}".format(
        reduce(mul, map(lambda x: x.tile_id, corner_tiles), 1)))

    #  assembling the whole image, start from one corner tile, assemble the first row
    #  then use the first row as anchor,  find the next 11 rows
    current_tile = corner_tiles[0]
    anchor_corner_boarders = [
        b for b in current_tile.get_boarders()
        if len(boarder_to_tile_mapping[b]) == 1
    ]
    # fix left anchor boarder
    left_anchor, up_anchor = anchor_corner_boarders[0], anchor_corner_boarders[1]
    # tansform current tile to make left_anchor appear left
    current_tile.arange_tile_to_match_boarders(left_anchor, 2)

    #  if up_anchor appears down in current tite, flip vertically
    boarders = current_tile.get_boarders()
    if up_anchor not in boarders:
        up_anchor = up_anchor[::-1]

    #  if up_anchor not in boarders:
        #  raise Exception("shit")

    up_anchor_idx = current_tile.get_boarders().index(up_anchor)
    if up_anchor_idx not in [0, 1]:
        raise Exception("Something wrong about up anchor")
    if boarders.index(up_anchor) == 1:
        current_tile.tile_array = flip_vertical(current_tile.tile_array)
        left_anchor = current_tile.get_boarders()[2]

    assert current_tile.get_boarders()[2] == left_anchor, "shit happens"
    first_row, known_tiles = [current_tile], set([current_tile])
    for i in range(11):
        left_anchor = current_tile.get_opposite_boarder(left_anchor)
        next_tiles = [
            t for t in boarder_to_tile_mapping[left_anchor]
            if t not in known_tiles
        ]
        if len(next_tiles) != 1:
            raise Exception("Something is wrong")
        current_tile = next_tiles[0]
        current_tile.arange_tile_to_match_boarders(left_anchor, 2)
        current_boarders = current_tile.get_boarders()
        first_row.append(current_tile)
        known_tiles.add(current_tile)
    assert len(first_row) == 12, "first row should have 12 tiles"

    image_grid, previous_row = [first_row], first_row
    for i in range(11):
        up_boarders = [t.get_boarders()[1] for t in previous_row]
        row = []
        for anchor in up_boarders:
            next_tiles = [
                t for t in boarder_to_tile_mapping[anchor]
                if t not in known_tiles
            ]
            if len(next_tiles) != 1:
                raise Exception("Something is wrong: {}".format(len(next_tiles)))
            row.append(next_tiles[0])
            known_tiles.add(next_tiles[0])
            next_tiles[0].arange_tile_to_match_boarders(anchor, 0)
        image_grid.append(row)
        previous_row = row
    assert len(known_tiles) == 144, "all tiles positions must be known"
    return image_grid


def concat_array(*arrays, orient="h"):
    # concat horizontally
    if orient == "h" or orient == 'H':
        new_array = []
        for i in range(len(arrays[0])):
            new_row = []
            for arr in arrays:
                new_row += arr[i]
            new_array.append(new_row)
        return new_array
    elif orient == "v" or orient == "V":
        new_array = [row for arr in arrays for row in arr]
        return new_array
    else:
        raise NotImplemented("Concat {} not implemented".format(orient))


def assemble_image(image_grid, remove_boarders=True):
    image_rows = []
    for row in image_grid:
        if remove_boarders:
            image_rows.append(
                concat_array(*[tile.remove_boarders() for tile in row],
                             orient="h"))
        else:
            image_rows.append(
                concat_array(*[tile.tile_array for tile in row], orient="h"))
    return concat_array(*image_rows, orient="v")


def part_2(image):
    # load sea monster
    input_path = Path(__file__).parent / "monster.txt"
    with input_path.open("r") as f:
        content = f.read()
    monster = [list(ln) for ln in content.split("\n") if ln != ""]
    monster_width, monster_height = len(monster[0]), len(monster)
    image_width, image_height = len(image[0]), len(image)
    image_tile = Tile(100, image)

    def search_monster(image_array):
        found_monsters = []
        width_steps = image_width - monster_width + 1
        height_steps = image_height - monster_height + 1
        for i in range(height_steps):
            for j in range(width_steps):
                if all(monster[m][n] == " "
                       or image_array[i + m][j + n] == monster[m][n]
                       for m in range(monster_height)
                       for n in range(monster_width)):
                    found_monsters.append((i, j))
        return found_monsters

    def replace_images(image_array, monster_up_corner_indexes):
        for i, j  in monster_up_corner_indexes:
           for m in range(monster_height):
               for n in range(monster_width):
                   if monster[m][n] == "#":
                       image_array[i+m][j+n] = "O"
        return image_array

    for i, tile in enumerate(image_tile.transforms()):
        image_array = tile.tile_array
        found_monsters = search_monster(image_array)
        print("Found monsters: {}".format(found_monsters))
        if len(found_monsters) != 0:
            image_array = [
                list(arr) for arr in image_array
            ]
            image_array = replace_images(image_array, found_monsters)
            count = 0
            for i in range(len(image_array)):
                for j in range(len(image_array[0])):
                    if image_array[i][j] == "#":
                        count += 1
            return count


if __name__ == '__main__':
    tiles = Tile.load_tiles_from_file("input.txt")
    image_grid = part_1(tiles)
    image = assemble_image(image_grid)

    assert len(image) == 96
    assert len(image[0]) == 96
    print("Answer to part 2: {}".format(part_2(image)))
