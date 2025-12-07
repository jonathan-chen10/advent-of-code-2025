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
  
  def has_num(self, query: int) -> bool:
    return self.any_true(lambda ran : ran[0] <= query <= ran[1])
  
  def ranges_disjoint(self) -> list[tuple[int, int]]:
    res = []
    for ran in sorted(self.ranges, key = lambda r : r[0]):
      if len(res) == 0:
        res.append(ran)
      else:
        last = res[-1]
        if last[1] < ran[0] - 1:
          res.append(ran)
        else:
          res[-1] = (last[0], max(last[1], ran[1]))
    return res
  
  def total_length(self) -> int:
    return sum(r[1] - r[0] + 1 for r in self.ranges_disjoint())  

def solve_A(input_lines: list[str]) -> int:
  ranges = RangeSet()
  ingredients = []
  for line in input_lines:
    if '-' in line:
      start, end = [int(n) for n in line.split('-')]
      ranges.add_range(start, end)
    elif len(line.strip()) > 0:
      ingredients.append(int(line))
  
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
