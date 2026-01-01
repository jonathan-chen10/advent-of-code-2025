from dataclasses import dataclass
from functools import cached_property
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list[str]) -> int:
  counter = 0
  shapes: list[Polyomino] = []
  reading_shape = False
  current_shape: list[list[bool]] = []
  for line in input_lines:
    line = line.strip()
    if len(line) == 0:
      assert len(current_shape) > 0
      assert (len(l) == len(current_shape[0]) for l in current_shape)
      shapes.append(Polyomino(current_shape))
      current_shape = []
      reading_shape = False 
    elif line[-1] == ':':
      reading_shape = True 
    elif reading_shape:
      current_shape.append([True if c == '#' else False for c in line])
    else:
      dims, *reqs = line.split()
      reqs = [int(n) for n in reqs]
      dims = tuple([int(n) for n in dims[:-1].split('x')])
      if fit(dims[0], dims[1], shapes, reqs):
        counter += 1
  assert counter > 477
  return counter 

def fit(width: int, height: int, shapes: list[Polyomino], reqs: list[int]) -> bool:
  if fit_rects(width, height, [s.dim() for s in shapes], reqs):
    return True 
  if sum(p.area * n for p, n in zip(shapes, reqs)) > width * height:
    return False 
  print("Optimizing...")
  return False 

def fit_rects(width: int, height: int, sizes: list[tuple[int, int]], amt: list[int]) -> bool:
  #print(width, height, amt)
  assert len(sizes) == len(amt)
  if len(amt) == 0 or sum(amt) == 0:
    return True
  if width == 0 or height == 0:
    return False
  sizes = [s for i, s in enumerate(sizes) if amt[i] != 0]
  amt = [a for i, a in enumerate(amt) if amt[i] != 0]
  if len(amt) == 0:
    return True
  if len(set(sizes)) != len(sizes):
    new_map = {}
    for d, n in zip(sizes, amt):
      if d in new_map:
        new_map[d] += n 
      else:
        new_map[d] = n 
    new_sizes = []
    new_amt = []
    for k, v in new_map.items():
      new_sizes.append(k)
      new_amt.append(v)
    return fit_rects(width, height, new_sizes, new_amt)
  # we'll start by just using the same shape
  best_leftover = max(width, height)
  candidate_width = None 
  candidate_height = None
  candidate_amt = None
  for i, rect in sorted(enumerate(sizes), key=lambda s: s[1][0] * s[1][1], reverse=True):
    if height - rect[1] >= 0:
      qw = width // rect[0]
      rw = width % rect[0] 
      if rw == 0:
        amt[i] = max(0, amt[i] - qw)
        return fit_rects(width, height - rect[1], sizes, amt)
      elif rw < best_leftover:
        best_leftover = rw 
        candidate_width = width 
        candidate_height = height - rect[1]
        candidate_amt = amt[:i] + [max(0, amt[i] - qw)] + amt[i+1:]
    if height - rect[0] >= 0:
      qw = width // rect[1]
      rw = width % rect[1] 
      if rw == 0:
        amt[i] = max(0, amt[i] - qw)
        return fit_rects(width, height - rect[0], sizes, amt)
      elif rw < best_leftover:
        best_leftover = rw 
        candidate_width = width 
        candidate_height = height - rect[0]
        candidate_amt = amt[:i] + [max(0, amt[i] - qw)] + amt[i+1:]
    if width - rect[1] >= 0:
      qw = height // rect[0]
      rw = height % rect[0] 
      if rw == 0:
        amt[i] = max(0, amt[i] - qw)
        return fit_rects(width - rect[1], height, sizes, amt)
      elif rw < best_leftover:
        best_leftover = rw 
        candidate_width = width - rect[1]
        candidate_height = height
        candidate_amt = amt[:i] + [max(0, amt[i] - qw)] + amt[i+1:]
    if width - rect[0] >= 0:
      qw = height // rect[1]
      rw = height % rect[1] 
      if rw == 0:
        amt[i] = max(0, amt[i] - qw)
        return fit_rects(width - rect[0], height, sizes, amt)
      elif rw < best_leftover:
        best_leftover = rw 
        candidate_width = width - rect[0]
        candidate_height = height
        candidate_amt = amt[:i] + [max(0, amt[i] - qw)] + amt[i+1:]
  if best_leftover == min(width, height):
    return False
  assert candidate_amt is not None and candidate_height is not None and candidate_width is not None
  #print(height - candidate_height, width - candidate_width)
  return fit_rects(candidate_width, candidate_height, sizes, candidate_amt)



class Polyomino():
  shape: list[list[bool]]

  def __init__(self, shape: list[list[bool]]):
    assert (True in shape[0] and True in shape[-1] 
            and True in [r[0] for r in shape] 
            and True in [r[-1] for r in shape])
    self.shape = shape

  def dim(self) -> tuple[int, int]:
    return (len(self.shape), len(self.shape[0]))
  
  @cached_property
  def area(self) -> int:
    return sum(sum(row) for row in self.shape)

  

def solve_B(input_lines: list[str]) -> int:
  raise NotImplementedError()

if __name__ == '__main__':
  main_day(12)
