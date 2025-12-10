import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day
from utils.ranges import RangeSet

def solve_A(input_lines: list[str]) -> int:
  ranges = RangeSet()
  ingredients = []
  for line in input_lines:
    if '-' in line:
      start, end = [int(n) for n in line.split('-')]
      ranges.add_range(start, end)
    elif len(line.strip()) > 0:
      ingredients.append(int(line))
  ranges.merge_ranges()
  
  return sum(1 for id in ingredients if ranges.has_num(id))

def solve_B(input_lines: list[str]) -> int:
  ranges = RangeSet()
  for line in input_lines:
    if '-' in line:
      start, end = [int(n) for n in line.split('-')]
      ranges.add_range(start, end)
    if len(line.strip()) == 0:
      break
  
  return ranges.total_length()

if __name__ == '__main__':
  main_day(5)
