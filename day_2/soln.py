import argparse
import os
import sys

sys.path.append('..')
this_dir = os.path.dirname(__file__)

def solve_A(input_lines: list) -> int:
  ranges = input_lines[0].split(',') 
  sum = 0
  for r in ranges:
    start_s, end_s = r.split('-')
    first_pre = next_pre_s(start_s)
    last_pre = prev_pre_s(end_s)
    for n in range(int(first_pre), int(last_pre) + 1):
      sum += int(str(n) * 2)
  return sum 

def next_pre_s(sn: str) -> str:
  if len(sn) % 2 != 0:
    # smallest repeating number with d+1 digits
    return '1' + '0' * (len(sn) // 2)
  candidate_half_s = sn[:len(sn) // 2]
  candidate = int(candidate_half_s + candidate_half_s)
  if candidate >= int(sn):
    return candidate_half_s
  else:
    return str(int(candidate_half_s) + 1)

def prev_pre_s(sn: str) -> str:
  if len(sn) % 2 != 0:
    # largest repeating number with d-1 digits
    return '9' * (len(sn) // 2)
  candidate_half_s = sn[:len(sn) // 2]
  candidate = int(candidate_half_s + candidate_half_s)
  if candidate <= int(sn):
    return candidate_half_s
  else:
    return str(int(candidate_half_s) - 1)

def solve_B(input_lines: list):
  pass

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
