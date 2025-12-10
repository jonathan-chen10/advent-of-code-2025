import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list) -> int:
  ranges = input_lines[0].split(',') 
  sum = 0
  for r in ranges:
    start_s, end_s = r.split('-')
    first_pre = next_pre_s(start_s, 2)
    last_pre = prev_pre_s(end_s, 2)
    for n in range(int(first_pre), int(last_pre) + 1):
      sum += int(str(n) * 2)
  return sum 

def next_pre_s(sn: str, num_reps) -> str:
  if len(sn) % num_reps != 0:
    # smallest repeating number with d+1 digits
    return '1' + '0' * (len(sn) // num_reps)
  candidate_atom_s = sn[:len(sn) // num_reps]
  candidate = int(candidate_atom_s * num_reps)
  if candidate >= int(sn):
    return candidate_atom_s
  else:
    return str(int(candidate_atom_s) + 1)

def prev_pre_s(sn: str, num_reps) -> str:
  if len(sn) % num_reps != 0:
    # largest repeating number with d-1 digits
    return '9' * (len(sn) // num_reps)
  candidate_atom_s = sn[:len(sn) // num_reps]
  candidate = int(candidate_atom_s * num_reps)
  if candidate <= int(sn):
    return candidate_atom_s
  else:
    return str(int(candidate_atom_s) - 1)

def solve_B(input_lines: list):
  ranges = input_lines[0].split(',') 
  sum = 0
  for r in ranges:
    start_s, end_s = r.split('-')
    for num_reps in range(2, len(end_s) + 1):
      first_pre = next_pre_s(start_s, num_reps)
      last_pre = prev_pre_s(end_s, num_reps)
      for n in range(int(first_pre), int(last_pre) + 1):
        if not repeating_num(n):
          sum += int(str(n) * num_reps)
  return sum 

def repeating_num(n: int) -> bool:
  sn = str(n)
  for num_reps in range(2, len(sn) + 1):
    if sn == sn[:len(sn) // num_reps] * num_reps:
      return True
  return False

if __name__ == '__main__':
  main_day(2)
