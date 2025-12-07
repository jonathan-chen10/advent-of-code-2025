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
  assert len(input_lines) > 0
  for line in input_lines:
    assert len(line) == len(input_lines[0])

  running_sum = 0
  buffer = []
  for col in range(len(input_lines[0])-1, -1, -1):
    # read number
    this_num_s = ''
    for row in range(len(input_lines)):
      if input_lines[row][col].isdigit():
        this_num_s += input_lines[row][col]
    if len(this_num_s) > 0:
      buffer.append(int(this_num_s))

    # perform operation
    if input_lines[len(input_lines) - 1][col] == '+':
      running_sum += sum(buffer)
      buffer = []
    elif input_lines[len(input_lines) - 1][col] == '*':
      prod = 1
      for n in buffer:
        prod *= n
      running_sum += prod
      buffer = []
      
  return running_sum

if __name__ == '__main__':
  main_day(6)
