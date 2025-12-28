from functools import cache
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
  return count_paths_dfs_dag('you', 'out', stack, adj)

def count_paths_dfs(cur: str, goal: str, stack: list[str], 
                    adj_list: dict[str, list[str]],
                    must_pass: list[str] = []) -> int:
  if cur == goal:
    return 1 if all(v in stack for v in must_pass) else 0
  neighbors = adj_list[cur]
  ctr = 0 
  for v in neighbors:
    if v not in stack:
      ctr += count_paths_dfs(v, goal, stack + [cur], adj_list, must_pass)
  return ctr

def count_paths_dfs_dag(cur: str, goal: str, checkpoints_seen: list[str], 
                    adj_list: dict[str, list[str]],
                    checkpoints: list[str] = []) -> int:
  @cache
  def proc(cur: str, checkpoints_seen: tuple[str]):
    if cur == goal:
      return 1 if len(checkpoints_seen) == len(checkpoints) else 0
    neighbors = adj_list[cur]
    ctr = 0 
    for v in neighbors:
      ctr += proc(
        v, 
        (tuple([*checkpoints_seen, cur]) 
         if cur in checkpoints else checkpoints_seen), 
      )
    return ctr
  
  return proc(cur, tuple(checkpoints_seen))
  

def solve_B(input_lines: list[str]) -> int:
  adj: dict[str, list[str]] = {}
  for line in input_lines:
    toks = line.split()
    adj[toks[0][:-1]] = toks[1:]
  stack: list[str] = []
  return count_paths_dfs_dag('svr', 'out', stack,  adj, ['dac', 'fft'])

if __name__ == '__main__':
  main_day(11)
