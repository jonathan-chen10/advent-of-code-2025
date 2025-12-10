import re
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list[str]) -> int:
  sum = 0
  for prob in input_lines:
    goal, buttons, _ = parse_problem(prob)
    memo: dict[tuple[int, ...], set[int]] = {
      () : set()
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
  assert(re_match)

  goal = set([i for i, ltr in enumerate(re_match.group(1)) if ltr == '#'])
  buttons = [[int(n) for n in button_str[1:-1].split(',')] 
             for button_str in re_match.group(2).split()]
  joltages = [int(n) for n in re_match.group(3).split(',')]

  return goal, buttons, joltages

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
  raise NotImplementedError()

if __name__ == '__main__':
  main_day(10)
