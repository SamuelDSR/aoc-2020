#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque


def load_input():
    player_a_seq = [
        41, 48, 12, 6, 1, 25, 47, 43, 4, 35, 10, 13, 23, 39, 22, 28, 44, 42,
        32, 31, 24, 50, 34, 29, 14
    ]

    player_b_seq = [
        36, 49, 11, 16, 20, 17, 26, 30, 18, 5, 2, 38, 7, 27, 21, 9, 19, 15, 8,
        45, 37, 40, 33, 46, 3
    ]
    return player_a_seq, player_b_seq


def part_1(player_a_seq, player_b_seq):
    player_a_deck = deque(player_a_seq)
    player_b_deck = deque(player_b_seq)
    fingerprint_of_a = [c for c in player_a_deck]

    while len(player_a_deck) != 0 and len(player_b_deck) != 0:
        a_draw = player_a_deck.popleft()
        b_draw = player_b_deck.popleft()
        if a_draw > b_draw:
            player_a_deck.append(a_draw)
            player_a_deck.append(b_draw)
        else:
            player_b_deck.append(b_draw)
            player_b_deck.append(a_draw)

        # check infinite loop
        if [c for c in player_a_deck] == fingerprint_of_a:
            print("Going to an infinite loop!")
            return None, True

    if len(player_a_deck) != 0:
        final_deck, ret = player_a_deck, True
    else:
        final_deck, ret = player_b_deck, False
    return final_deck, ret


def sum_deck(deck):
    return sum(
        [x * y for x, y in zip(deck, reversed(range(1,
                                                    len(deck) + 1)))])


def part_2(player_a_seq, player_b_seq):
    def part_2_util(a_seq, b_seq):
        seens = set()
        player_a_deck, player_b_deck = deque(a_seq), deque(b_seq)
        while len(player_a_deck) != 0 and len(player_b_deck) != 0:
            # before draw, check infinite loop
            fingerprint = (tuple(player_a_deck), tuple(player_b_deck))
            if fingerprint in seens:
                return True, player_a_deck, player_b_deck
            else:
                seens.add(fingerprint)

            a_draw = player_a_deck.popleft()
            b_draw = player_b_deck.popleft()
            # going to a subgame
            if len(player_a_deck) >= a_draw and len(player_b_deck) >= b_draw:
                a_deck_copy = [c for c in player_a_deck][:a_draw]
                b_deck_copy = [c for c in player_b_deck][:b_draw]
                sub_ret, _, _ = part_2_util(a_deck_copy, b_deck_copy)
                if sub_ret:
                    player_a_deck.append(a_draw)
                    player_a_deck.append(b_draw)
                else:
                    player_b_deck.append(b_draw)
                    player_b_deck.append(a_draw)
            elif a_draw > b_draw:
                player_a_deck.append(a_draw)
                player_a_deck.append(b_draw)
            else:
                player_b_deck.append(b_draw)
                player_b_deck.append(a_draw)

        # game finished
        if len(player_a_deck) > 0:
            return True, player_a_deck, player_b_deck
        return False, player_a_deck, player_b_deck

    ret, final_a_deck, final_b_deck = part_2_util(player_a_seq, player_b_seq)
    if ret:
        return sum_deck(final_a_deck)
    return sum_deck(final_b_deck)


if __name__ == '__main__':
    player_a_seq, player_b_seq = load_input()
    final_deck, ret = part_1(player_a_seq, player_b_seq)
    print("Answer to part 1: {}".format(sum_deck(final_deck)))

    # infinite loop
    ret = part_2(player_a_seq, player_b_seq)
    print("Answer to part 2: {}".format(ret))
