import argparse
from collections.abc import Callable
import os
import sys

sys.path.append('..')
this_dir = os.path.dirname(__file__)

def solve_A(input_lines: list[str]) -> int:
  counter = 0
  for row in range(len(input_lines)):
    for col in range(len(input_lines[0])):
      if (input_lines[row][col] == '@' and 
          count_neighboring(input_lines, row, col, lambda c : c == '@') < 4):
        counter += 1
  return counter 

def count_neighboring(input_lines: list[str], 
                      row: int, col: int, pred: Callable[[str], bool]) -> int:
  assert 0 <= row < len(input_lines)
  assert 0 <= col < len(input_lines[0])
  directions_y = [0]
  if row != 0:
    directions_y.append(-1)
  if row != len(input_lines) - 1:
    directions_y.append(1)
  directions_x = [0]
  if col != 0:
    directions_x.append(-1)
  if col != len(input_lines[0]) - 1:
    directions_x.append(1)

  counter = 0
  for dy in directions_y:
    for dx in directions_x:
      if (not (dx == 0 and dy == 0) and pred(input_lines[row + dy][col + dx])):
        counter += 1

  return counter

def solve_B(input_lines: list[str]) -> int:
  raise NotImplementedError()

if __name__ == '__main__':
  argparser = argparse.ArgumentParser()
  argparser.add_argument('mode', choices=['test', 'run'])
  argparser.add_argument('stage', choices=['A', 'B'])
  args = argparser.parse_args()

  if args.mode == "test":
    with open(f"{this_dir}/input-{args.stage.lower()}-test.txt", "r") as file:
      input_lines = [line.rstrip() for line in file.readlines()] 
  else:
    input_lines = [line.rstrip() for line in sys.stdin]
  
  if args.stage == "A":
    result = solve_A(input_lines)
  else:
    result = solve_B(input_lines)
  
  if args.mode == "test":
    with open(f"{this_dir}/output-{args.stage.lower()}-test.txt", "r") as file:
      expected_result = int(file.read())
      print("Test passed!" if result == expected_result else "Test failed!")
      print(f"Expected: {expected_result}")
      print(f"Got: {result}")
  else:
    print(result)
