import os
import sys
from typing import cast

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list[str]) -> int:
  points = [tuple(int(n) for n in line.split(',')) for line in input_lines]
  cur_max = 0
  for a in points:
    for b in points:
      cur_max = max(cur_max, (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1))
  return cur_max

def solve_B(input_lines: list[str]) -> int:
  points = [tuple(int(n) for n in line.split(',')) for line in input_lines]
  for p in points:
    assert len(p) == 2
  points = cast(list[tuple[int, int]], points)

  cur_max = 0
  for a in points:
    for b in points:
      if valid_rectangle(points, a, b):
        cur_max = max(cur_max, (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1))
  return cur_max

def valid_rectangle(points: list[tuple[int, int]], 
                    a: tuple[int, int], b: tuple[int, int]):
  min_x = min(a[0], b[0])
  max_x = max(a[0], b[0])
  min_y = min(a[1], b[1])
  max_y = max(a[1], b[1])
  # postulate: for all qualified rectangles...
  # 1. no other lines pass through any interior point (edge is OK)
  for i in range(len(points) - 1):
    start = points[i]
    end = points[i+1]
    if not (start[0] <= min_x and end[0] <= min_x or 
            start[0] >= max_x and end[0] >= max_x or 
            start[1] <= min_y and end[1] <= min_y or 
            start[1] >= max_y and end[1] >= max_y):
      return False

  # 2. any strictly interior point is inside the polygon (ray casting)
  if a[0] == b[0] or a[1] == b[1]:
    return True
  intersections_right = 0
  interior = (min_x + 0.5, min_y + 0.5)

  for i in range(len(points) - 1):
    start = points[i]
    end = points[i+1]
    if (start[1] == end[1] and start[1] > interior[1] and
        min(start[0], end[0]) < interior[0] < max(start[0], end[0])):
      intersections_right += 1
  
  return intersections_right % 2 == 1


if __name__ == '__main__':
  main_day(9)
