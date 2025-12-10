from collections.abc import Sequence
import os
import sys

from utils.grid import CellularAutomaton

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from runner import main_day

def solve_A(input_lines: list[str]) -> int:
  assert len(input_lines) > 0
  for line in input_lines:
    assert len(line) == len(input_lines[0])

  grid = [list(row) for row in input_lines]
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      stream_top = (grid[row][col] == '.' 
                    and (grid[max(row - 1, 0)][col] in ['|', 'S']))
      split_left = (grid[row][col] == '.' 
                    and grid[row][min(col + 1, len(grid[0]) - 1)] == '^'
                    and grid[max(row - 1, 0)][min(col + 1, len(grid[0]) - 1)] == '|')
      split_right = (grid[row][col] == '.' 
                     and grid[row][max(col - 1, 0)] == '^'
                     and grid[max(row - 1, 0)][max(col - 1, 0)] == '|')
      if stream_top or split_left or split_right:
        grid[row][col] = '|' 

  counter = 0
  for row in range(1, len(grid)):
    for col in range(len(grid[0])):
      if grid[row][col] == '^' and grid[row - 1][col] == '|':
        counter += 1
  return counter


def solve_B(input_lines: list[str]) -> int:
  assert len(input_lines) > 0
  for line in input_lines:
    assert len(line) == len(input_lines[0])

  grid = [list(row) for row in input_lines]
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      stream_top = (grid[row][col] == '.' 
                    and (grid[max(row - 1, 0)][col] in ['|', 'S']))
      split_left = (grid[row][col] == '.' 
                    and grid[row][min(col + 1, len(grid[0]) - 1)] == '^'
                    and grid[max(row - 1, 0)][min(col + 1, len(grid[0]) - 1)] == '|')
      split_right = (grid[row][col] == '.' 
                     and grid[row][max(col - 1, 0)] == '^'
                     and grid[max(row - 1, 0)][max(col - 1, 0)] == '|')
      if stream_top or split_left or split_right:
        grid[row][col] = '|' 

  streams = [1]
  for row in range(1, len(grid) - 1, 2):
    next_streams = []
    stream_num = 0
    for col in range(len(grid[0])):
      if grid[row][col] == '|':
        if (grid[row + 1][col] == '^' and 
            ((grid[row + 1][max(col - 2, 0)] == '^' and 
              grid[row][max(col - 2, 0)] == '|') or 
             grid[row][col - 1] == '|')):
          next_streams[-1] += streams[stream_num]
          next_streams.append(streams[stream_num])
        elif grid[row + 1][col] == '^':
          next_streams.append(streams[stream_num])
          next_streams.append(streams[stream_num])
        elif (grid[row + 1][col - 1] == '^' and grid[row][col - 1] == '|'):
          next_streams[-1] += streams[stream_num]
        else:
          next_streams.append(streams[stream_num])
        stream_num += 1
    streams = next_streams

  return sum(streams)

if __name__ == '__main__':
  main_day(7)
