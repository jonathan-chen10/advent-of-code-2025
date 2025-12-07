from collections.abc import Callable
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

class RangeSet():
  """Represents a collection of ranges, where each range is inclusive."""
  
  def __init__(self, data: list[tuple[int, int]] | None = None):
    if data is None:
      self.ranges: list[tuple[int, int]] = []
    else:
      self.ranges: list[tuple[int, int]] = list(data)

  def add_range(self, start: int, end: int) -> None:
    self.ranges.append((start, end))

  def any_true(self, pred: Callable[[tuple[int, int]], bool]) -> bool:
    return any(pred(r) for r in self.ranges)
  
  def all_true(self, pred: Callable[[tuple[int, int]], bool]) -> bool:
    return all(pred(r) for r in self.ranges)

  

def solve_A(input_lines: list[str]) -> int:
  ranges = RangeSet()
  ingredients = []
  for line in input_lines:
    if '-' in line:
      start, end = [int(n) for n in line.split('-')]
      ranges.add_range(start, end)
    elif len(line.strip()) > 0:
      ingredients.append(int(line))
  
  return sum(1 for id in ingredients 
             if ranges.any_true(lambda ran : ran[0] <= id <= ran[1]))


def solve_B(input_lines: list[str]) -> int:
  raise NotImplementedError()

if __name__ == '__main__':
  main_day(5)
