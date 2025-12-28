import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list[str]) -> int:
  adj: dict[str, list[str]] = {}
  for line in input_lines:
    toks = line.split()
    adj[toks[0][:-1]] = toks[1:]
  stack: list[str] = []
  return count_paths_dfs('you', stack, adj)

def count_paths_dfs(cur: str, stack: list[str], adj_list: dict[str, list[str]]):
  if cur == 'out':
    return 1
  neighbors = adj_list[cur]
  ctr = 0 
  for v in neighbors:
    if v not in stack:
      ctr += count_paths_dfs(v, stack + [cur], adj_list)
  return ctr
  

def solve_B(input_lines: list[str]) -> int:
  raise NotImplementedError()

if __name__ == '__main__':
  main_day(11)
