
from fractions import Fraction

from functools import cache
from math import prod
import re
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils.matrix import Array2D, rref
from runner import main_day


def solve_A(input_lines: list[str]) -> int:
    sum = 0
    for prob in input_lines:
        goal, buttons, _ = parse_problem(prob)
        memo: dict[tuple[int, ...], set[int]] = {
            (): set()
        }
        selection = []
        for _ in range(2**(len(buttons))):
            if len(selection) == len(set(selection)):
                # any subset will be in memo
                if len(selection) > 0:
                    prev = memo[tuple(sorted(selection[:-1]))]
                    cur = flip(prev, set(buttons[selection[-1]]))
                else:
                    cur = set()
                if cur == goal:
                    sum += len(selection)
                    break
                else:
                    memo[tuple(selection)] = cur
                    try:
                        selection = next_selection(selection, len(buttons))
                    except AssertionError:
                        raise ValueError(f"Problem UNSAT: {prob}")
    return sum


def parse_problem(prob: str) -> tuple[set[int], list[list[int]], list[int]]:
    re_match = re.search(r'\[(.+)\] (.+) \{(.+)\}', prob)
    assert (re_match)

    lights = set([i for i, ltr in enumerate(re_match.group(1)) if ltr == '#'])
    buttons = [[int(n) for n in button_str[1:-1].split(',')]
               for button_str in re_match.group(2).split()]
    joltages = [int(n) for n in re_match.group(3).split(',')]

    return lights, buttons, joltages


def next_selection(selection: list[int], base: int) -> list[int]:
    asc = [i for i in range(base)]
    assert selection != asc

    if len(selection) == 0:
        return [0]

    r = selection.copy()
    if selection == asc[-len(selection):]:
        return [i for i in range(len(selection) + 1)]
    else:
        idx = len(selection) - 1
        threshold = base - 1
        while r[idx] == threshold:
            r[idx] = -1
            threshold -= 1
            idx -= 1
        r[idx] += 1
        for idx, val in enumerate(r):
            if val == -1:
                r[idx] = r[idx - 1] + 1
    return r


def flip(a: set[int], b: set[int]) -> set[int]:
    return (a | b) - (a & b)


def solve_B(input_lines: list[str]) -> int:
    total = 0
    for prob in input_lines:
        _, buttons, goal = parse_problem(prob)
        # build matrix
        a = Array2D.zeros(len(goal), len(buttons) + 1)
        for i, button in enumerate(buttons):
            for light in button:
                a.arr[light][i] = Fraction(1)
        for light, target in enumerate(goal):
            a.arr[light][-1] = Fraction(target)
        # solve rref
        solved = rref(a)
        frees = solved.free_vars()

        # try all combinations of free variables
        # free variables should represent real buttons,
        # so they are limited by the min of the constraint
        # they add
        max_frees: list[int] = []
        for f in frees:
            m = max(goal) + 1
            button = buttons[f]
            for light in button:
                m = min(m, goal[light]) + 1
            max_frees.append(m)

        # start with brute force
        # Compute objective by choosing values of free variables,
        # checking integrality, and summing all variables
        ans = sum(goal)
        prev = None
        frees_coef = [[el for i, el in enumerate(row) if i in frees] for row in solved.arr]
        zeros_cutoff = len(solved.arr)
        for ri, row in enumerate(solved.arr):
            if all(n == 0 for n in row):
                zeros_cutoff = ri 
                break
        frees_assn: list[int] = [0 for _ in range(len(frees))]
        nonzero = False
        prev_tup = tuple(frees_assn[:-1])
        need_regroup = False
        bad_idx = None
        while sum(frees_assn) <= sum(max_frees):
            #print(frees_assn, nonzero, need_regroup)
            if tuple(frees_assn[:-1]) != prev_tup:
                nonzero = False 
                need_regroup = False
                prev_tup = tuple(frees_assn[:-1])
            if sum(frees_assn) > ans or need_regroup:
                if frees_assn == max_frees:
                    break
                regroup_inplace(frees_assn, max_frees)
                if sum(frees_assn) == 0:
                    break
                continue
            fixed_assn: list[int] = []
            any_zero = False
            any_frac = False
            short_circuit = False

            if bad_idx is not None:
                fixed_val = (solved.arr[bad_idx][-1] -
                             sum([assn * frees_coef[bad_idx][free_idx] 
                                  for free_idx, assn in enumerate(frees_assn)]))
                if fixed_val < 0 and nonzero:
                    need_regroup = True 
                if fixed_val < 0:
                    short_circuit = True
                    any_zero = True

            for ri, row in enumerate(solved.arr[:zeros_cutoff]):
                if short_circuit:
                    break
                fixed_val = (row[-1] -
                             sum([assn * frees_coef[ri][free_idx] 
                                  for free_idx, assn in enumerate(frees_assn)]))
                if fixed_val < 0 and nonzero:
                    need_regroup = True 
                if fixed_val < 0:
                    bad_idx = ri
                    any_zero = True
                    break
                if fixed_val.denominator != 1:
                    any_frac = True
                fixed_assn.append(int(fixed_val))
            if not any_zero:
                nonzero = True
            if any_zero or any_frac:
                if frees_assn == max_frees:
                    break
                next_assn_inplace(frees_assn, max_frees)
                continue
            obj = sum(frees_assn) + sum(fixed_assn)
            if len(frees_assn) > 0 and frees_assn[-1] == 0:
                prev = obj
            if len(frees_assn) > 0 and frees_assn[-1] == 1 and prev is not None and obj > prev: 
                if frees_assn == max_frees:
                    break
                regroup_inplace(frees_assn, max_frees)
                if sum(frees_assn) == 0:
                    break
                continue
            #if obj < ans:
            #    print("Updated objective")
            ans = min(ans, obj)
            if frees_assn == max_frees:
                break
            next_assn_inplace(frees_assn, max_frees)
        total += ans
        #print(ans, total)
    return total

def regroup_inplace(frees_assn: list[int], max_frees: list[int], 
                    cur_idx: int | None = None) -> None:
    assert len(frees_assn) == len(max_frees)
    if cur_idx == None:
        cur_idx = len(frees_assn) - 1
    if cur_idx < 0:
        return
    if frees_assn[cur_idx] == 0:
        regroup_inplace(frees_assn, max_frees, cur_idx - 1)
        return 
    frees_assn[cur_idx] = 0
    return next_assn_inplace(frees_assn, max_frees, cur_idx - 1)
    

def next_assn_inplace(frees_assn: list[int], max_frees: list[int], 
                      cur_idx: int | None = None) -> None:
    assert len(frees_assn) == len(max_frees)
    if cur_idx == None:
        cur_idx = len(frees_assn) - 1
    if cur_idx < 0:
        return
    if frees_assn[cur_idx] < max_frees[cur_idx]:
        frees_assn[cur_idx] += 1
        return 
    frees_assn[cur_idx] = 0
    next_assn_inplace(frees_assn, max_frees, cur_idx - 1)
    return

def solve_B_old(input_lines: list[str]) -> int:
    sum = 0
    for prob in input_lines:
        _, buttons, goal = parse_problem(prob)
        print(f"# Buttons: {len(buttons)}, Goal: {goal}")
        ans = vector_knapsack(tuple(tuple(b) for b in buttons), tuple(goal))
        vector_knapsack.cache_clear()
        assert (ans != None)
        sum += ans
    return sum


@cache
def vector_knapsack(buttons: tuple[tuple[int]], target: tuple[int]) -> int | None:
    # base case
    if all(n == 0 for n in target):
        return 0

    candidate = sum(target) + 1

    for button in sorted(buttons, key=lambda b: sum(b), reverse=True):
        if all(target[i] > 0 for i in button):
            sub_problem = vector_knapsack(
                buttons,
                tuple(n - 1 if i in button else n for i, n in enumerate(target)))

            if sub_problem is not None:
                candidate = min(candidate, sub_problem + 1)

    if candidate > sum(target):
        # print(f"Fail {target}")
        return None
    print(f"DP {target} {candidate}")
    return candidate


if __name__ == '__main__':
    main_day(10)
