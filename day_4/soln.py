from collections.abc import Sequence
import os
import sys

from utils.grid import CellularAutomaton, count_neighboring

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

def solve_B(input_lines: list[str]) -> int:
  def transition_rule(grid: Sequence[Sequence[str]], row: int, col: int) -> str:
    if (grid[row][col] == '@' and 
        count_neighboring(grid, row, col, lambda c : c == '@') < 4):
      return '.'
    return grid[row][col]
  ca = CellularAutomaton(input_lines, transition_rule)
  ca.run()

  counter = 0
  for i in range(len(input_lines)):
    for j in range(len(input_lines[0])):
      if input_lines[i][j] != ca.current_state[i][j]:
        counter += 1

  return counter

if __name__ == '__main__':
  main_day(4)
