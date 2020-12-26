#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

def load_input():
    input_path = Path(__file__).parent / "input.txt"
    with Path(input_path).open('r') as f:
        lines = f.read()
    passports = lines.split("\n\n")
    passports = [
        dict(
            (t.split(":")[0], t.split(":")[1])
            for t in passport.strip().replace("\n", " ").split(" ")
        )
        for passport in passports
    ]
    return passports

def valid_passports_1(passports):
    ask_keys = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    valid = 0
    for p in passports:
        if len(ask_keys - set(p.keys())) == 0:
            valid += 1
    return valid

def valid_passports_2(passports):
    def _valid_range(value, minv, maxv):
        return value is not None and minv <= int(value) <= maxv

    valid = 0
    for p in passports:
        if not _valid_range(p.get("byr"), 1920, 2002):
            continue
        if not _valid_range(p.get("iyr"), 2010, 2020):
            continue
        if not _valid_range(p.get("eyr"), 2020, 2030):
            continue
        hgt = p.get("hgt")
        if hgt is None:
            continue
        if hgt.endswith("cm"):
            if not _valid_range(int(hgt[:-2]), 150, 193):
                continue
        elif hgt.endswith("in"):
            if not _valid_range(int(hgt[:-2]), 59, 76):
                continue
        else:
            continue

        hcl = p.get("hcl")
        if hcl is None or (not hcl.startswith("#")) or (not len(hcl) == 7):
            continue
        elements = set(hcl[1:])
        if len(elements - set([str(x) for x in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f'])) != 0:
            continue

        ecl = p.get("ecl")
        if ecl is None or not (ecl in set(["amb", "brn", "blu", "gry", "grn", "hzl", "oth"])):
            continue

        pid = p.get("pid")
        if pid is None or len(pid) != 9:
            continue
        try:
            int(pid)
        except:
            continue
        valid += 1
    return valid


if __name__ == '__main__':
    passports = load_input()

    print(valid_passports_1(passports))
    print(valid_passports_2(passports))
