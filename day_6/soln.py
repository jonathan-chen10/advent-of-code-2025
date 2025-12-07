import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list[str]) -> int:
  rows = []
  for line in input_lines[:-1]:
    rows.append([int(n) for n in line.split()])    
  ops = input_lines[-1].split()

  running_sum = 0
  for i, op in enumerate(ops):
    if op == '+':
      running_sum += sum([row[i] for row in rows])
    else:
      prod = 1
      for row in rows:
        prod *= row[i]
      running_sum += prod
  return running_sum



def solve_B(input_lines: list[str]) -> int:
  raise NotImplementedError()

if __name__ == '__main__':
  main_day(6)
