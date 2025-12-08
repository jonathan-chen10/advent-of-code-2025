from collections.abc import Callable

class RangeSet():
  """Represents a collection of ranges, where each range is inclusive."""
  
  def __init__(self, data: list[tuple[int, int]] | None = None):
    if data is None:
      self.ranges: list[tuple[int, int]] = []
    else:
      self.ranges: list[tuple[int, int]] = list(data)

  def merge_ranges(self) -> None:
    self.ranges = self.ranges_disjoint()

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
