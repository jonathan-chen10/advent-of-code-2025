from collections.abc import Callable, Sequence
import copy

class CellularAutomaton():
  def __init__(self, 
               grid: list[str] | list[list[str]], 
               rule: Callable[[Sequence[Sequence[str]], int, int], str]):
    self.original_state: list[list[str]] = [list(row) for row in grid]
    self.current_state: list[list[str]] = [list(row) for row in grid]
    self.rule: Callable[[Sequence[Sequence[str]], int, int], str] = rule

  def reset(self):
    self.current_state = copy.deepcopy(self.original_state)
  
  def step(self) -> bool:
    next_state = copy.deepcopy(self.current_state)
    updated = False 
    for row in range(len(self.current_state)):
      for col in range(len(self.current_state[0])):
        next_state[row][col] = self.rule(self.current_state, row, col)
        if next_state[row][col] != self.current_state[row][col]:
          updated = True 
    self.current_state = next_state
    return updated
  
  def run(self) -> None:
    while self.step():
      pass

def count_neighboring(grid: Sequence[Sequence[str]] | Sequence[str], 
                      row: int, col: int, pred: Callable[[str], bool]) -> int:
  assert 0 <= row < len(grid)
  assert 0 <= col < len(grid[0])
  directions_y = [0]
  if row != 0:
    directions_y.append(-1)
  if row != len(grid) - 1:
    directions_y.append(1)
  directions_x = [0]
  if col != 0:
    directions_x.append(-1)
  if col != len(grid[0]) - 1:
    directions_x.append(1)

  counter = 0
  for dy in directions_y:
    for dx in directions_x:
      if (not (dx == 0 and dy == 0) and pred(grid[row + dy][col + dx])):
        counter += 1

  return counter
