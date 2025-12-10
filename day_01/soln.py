import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list):
  state = 50
  counter = 0
  for line in input_lines:
    action = (1 if line[0] == "R" else -1) * int(line[1:])
    state = (state + action) % 100
    if state == 0:
      counter += 1
  return counter

def solve_B(input_lines: list):
  state = 50
  counter = 0
  for line in input_lines:
    action = (1 if line[0] == "R" else -1) * int(line[1:])
    temp_state = state + action
    if temp_state > 0:
      counter += temp_state // 100
    else:
      if state == 0:
        # don't double-count 0 by accident
        counter -= 1
      counter += -((temp_state - 1) // 100)
    state = temp_state % 100
  return counter

if __name__ == '__main__':
  main_day(1)
