#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path


def load_input(path):
    with Path(path).open('r') as f:
        lines = f.readlines()
    pattern = re.compile(r'(\d+|\+|\(|\)|\*)')
    return [pattern.findall(ln) for ln in lines]


def precedence(op):
    if op == '+':
        return 2
    elif op == '*':
        return 1
    else:
        return 0


def arthmetic_evaluation(v1, v2, op):
    if op == '+':
        return v1 + v2
    elif op == '*':
        return v1 * v2
    else:
        raise Exception("No such operator: {}".format(op))


def is_int(num_str):
    try:
        int(num_str)
        return True
    except:
        return False


def run(tokens, precedence, evaluator):
    """
    Classical stack machine, code copy from
    https://github.com/SamuelDSR/le-compte-est-bon/blob/master/eval_stack.py
    """
    value_stack, op_stack = [], []
    # evalute stack
    for t in tokens:
        t = t.strip()
        if is_int(t):
            value_stack.append(int(t))
        elif t == '(':
            op_stack.append(t)
        elif t == ')':
            while len(op_stack) != 0 and op_stack[-1] != '(':
                op = op_stack.pop()
                v2, v1 = value_stack.pop(), value_stack.pop()
                value_stack.append(evaluator(v1, v2, op))
            op_stack.pop()
        else:
            while len(op_stack) != 0 and op_stack[-1] != '(' and precedence(
                    op_stack[-1]) >= precedence(t):
                v2, v1 = value_stack.pop(), value_stack.pop()
                op = op_stack.pop()
                value_stack.append(evaluator(v1, v2, op))
            op_stack.append(t)
    # evalute left expressions
    while len(op_stack) != 0:
        v2, v1 = value_stack.pop(), value_stack.pop()
        op = op_stack.pop()
        value_stack.append(evaluator(v1, v2, op))
    return value_stack[-1]


def part_1(programs):
    return sum([run(p, lambda x: 1, arthmetic_evaluation) for p in programs])


def part_2(programs):
    return sum([run(p, precedence, arthmetic_evaluation) for p in programs])


if __name__ == '__main__':
    programs = load_input("day-18-input.txt")
    assert run(["1", "+", "2", "*", "3", "+", "4", "*", "5", "+", "6"],
               lambda x: 1, arthmetic_evaluation) == 71
    print(part_1(programs))
    print(part_2(programs))
