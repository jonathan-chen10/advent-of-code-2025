from collections.abc import Callable, Sequence
import copy
import math

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

class UnionFind():
  def __init__(self, coords: list[tuple[int, ...]]):
    self.coords = coords.copy()
    self.parent_idx = list(range(len(coords)))

  def find(self, idx: int) -> int:
    cur_idx = idx
    while (self.parent_idx[cur_idx] != cur_idx):
      cur_idx = self.parent_idx[cur_idx]
    return cur_idx 

  def union(self, i1: int, i2: int) -> bool:
    p1 = self.find(i1)
    p2 = self.find(i2)
    if p1 == p2:
      return False 
    self.parent_idx[p1] = p2 
    return True 
  
  def kruskal(self, 
              tries_limit: int | None = None, 
              unions_limit: int | None = None) -> list[tuple[int, int]]:
    pairs: list[tuple[tuple[int, tuple[int, ...]], 
                      tuple[int, tuple[int, ...]]]] = []
    
    for i1, b1 in enumerate(self.coords):
      for i2 in range(i1+1, len(self.coords)):
        b2 = self.coords[i2]
        pairs.append(((i1, b1), (i2, b2)))
    edges: list[tuple[int, int]] = [(x[0][0], x[1][0]) for x in sorted(
      pairs, key=lambda enums: l2(enums[0][1], enums[1][1])
    )]
    if tries_limit is not None:
      edges = edges[:tries_limit]

    edges_added = 0
    for i, edge in enumerate(edges):
      success_union = self.union(*edge)
      if success_union:
        edges_added += 1 
        if unions_limit is not None and edges_added == unions_limit:
          trace = edges[:i+1]
          return trace 
        elif self.connected():
          trace = edges[:i+1]
          return trace 
    return edges
        
  def connected(self):
    candidate = self.find(0)
    return all(self.find(i) == candidate 
               for i in range(1, len(self.parent_idx)))
        

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

def l2(x: tuple[int, ...], y: tuple[int, ...]):
  assert len(x) == len(y)
  return math.sqrt(sum((x[i]-y[i])**2 for i in range(len(x))))
