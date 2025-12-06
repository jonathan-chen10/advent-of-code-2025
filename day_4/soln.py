from collections.abc import Callable, Sequence
import os
import sys

parent_dir = os.path.abspath(
  os.path.join(os.path.dirname(__file__), '..')
)
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: Sequence[Sequence] | Sequence[str]) -> int:
  counter = 0
  for row in range(len(input_lines)):
    for col in range(len(input_lines[0])):
      if (input_lines[row][col] == '@' and 
          count_neighboring(input_lines, row, col, lambda c : c == '@') < 4):
        counter += 1
  return counter 

def count_neighboring(input_lines: Sequence[Sequence] | Sequence[str], 
                      row: int, col: int, pred: Callable[[str], bool]) -> int:
  assert 0 <= row < len(input_lines)
  assert 0 <= col < len(input_lines[0])
  directions_y = [0]
  if row != 0:
    directions_y.append(-1)
  if row != len(input_lines) - 1:
    directions_y.append(1)
  directions_x = [0]
  if col != 0:
    directions_x.append(-1)
  if col != len(input_lines[0]) - 1:
    directions_x.append(1)

  counter = 0
  for dy in directions_y:
    for dx in directions_x:
      if (not (dx == 0 and dy == 0) and pred(input_lines[row + dy][col + dx])):
        counter += 1

  return counter

def solve_B(input_lines: list[str]) -> int:
  arr = [list(row) for row in input_lines]
  counter = 0
  needs_checking = True 
  while needs_checking:
    needs_checking = False
    for row in range(len(arr)):
      for col in range(len(arr[0])):
        if (arr[row][col] == '@' and 
            count_neighboring(arr, row, col, lambda c : c == '@') < 4):
          needs_checking = True
          counter += 1
          arr[row][col] = '.'

  return counter

if __name__ == '__main__':
  main_day(4)
