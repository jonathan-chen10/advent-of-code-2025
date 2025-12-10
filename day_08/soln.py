from collections import Counter
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day
from utils.grid import UnionFind

def solve_A(input_lines: list[str]) -> int:
  n = int(input_lines[0])
  boxes = [tuple(int(coord) for coord in row.split(",")) for row in input_lines[1:]]
  uf = UnionFind(boxes)
  uf.kruskal(tries_limit = n)
  ctr = Counter(uf.find(i) for i in range(len(boxes)))

  r = 1
  for v in sorted(ctr.values(), reverse=True)[:3]:
    r *= v 
  return r

def solve_B(input_lines: list[str]) -> int:
  boxes = [tuple(int(coord) for coord in row.split(",")) for row in input_lines[1:]]
  uf = UnionFind(boxes)
  trace = uf.kruskal()
  return uf.coords[trace[-1][0]][0] * uf.coords[trace[-1][1]][0]

if __name__ == '__main__':
  main_day(8)
