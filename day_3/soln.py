import argparse
import os
import sys

sys.path.append('..')
this_dir = os.path.dirname(__file__)

def solve_A(input_lines: list) -> int:
  return sum([int(max_substring(bank, 2)) for bank in input_lines])

def max_substring(row: str, length: int) -> str:
  assert (len(row) >= length)
  if (length == 0):
    return ""
  if (len(row) == length):
    return row
  
  highest = chr(ord("0") - 1)
  loc = -1
  for i, c in enumerate(row[:len(row) - length + 1]):
    if c > highest:
      highest = c 
      loc = i 

  return highest + max_substring(row[loc + 1:], length - 1)

def solve_B(input_lines: list) -> int:
  return sum([int(max_substring(bank, 12)) for bank in input_lines])

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
