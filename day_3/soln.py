import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

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
  main_day(3)
