import argparse
import os
import sys

sys.path.append('..')
this_dir = os.path.dirname(__file__)

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
