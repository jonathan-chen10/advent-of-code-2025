import argparse
import os
import sys
import time

this_dir = os.path.dirname(__file__)

def solve_fxn(day: int, part: str):
  assert 1 <= day <= 12
  assert part in ['A', 'B']
  import importlib
  day_module = importlib.import_module(f'day_{day}.soln')
  return day_module.solve_A if part == 'A' else day_module.solve_B

def run_single(day: int, part: str, input_lines: list[str]):
  assert 1 <= day <= 12
  assert part in ['A', 'B']
  result = solve_fxn(day, part)(input_lines)
  print(result)

def test_single(day: int, part: str):
  assert 1 <= day <= 12
  assert part in ['A', 'B']
  with open(f"{this_dir}/day_{day}/input-{part}-test.txt", "r") as in_file:
    input_lines = [line.rstrip() for line in in_file.readlines()]
  result = solve_fxn(day, part)(input_lines)

  with open(f"{this_dir}/day_{day}/output-{part}-test.txt", "r") as out_file:
    expected_result = int(out_file.read())
    print("Test passed!" if result == expected_result else "Test failed!")
    print(f"Expected: {expected_result}")
    print(f"Got: {result}")

def time_single(day: int, part: str, input_lines: list[str]):
  assert 1 <= day <= 12
  assert part in ['A', 'B']
  start_time = time.perf_counter()
  solve_fxn(day, part)(input_lines)
  end_time = time.perf_counter()
  print(f"{end_time - start_time:.3f}")
    
def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument('mode', choices=['test', 'run', 'time', 'run_default', 'time_default'])
  argparser.add_argument('day', choices=[str(d) for d in range(1, 13)])
  argparser.add_argument('stage', choices=['A', 'B'])
  args = argparser.parse_args()
  
  if args.mode == "run":
    run_single(int(args.day), args.stage, [line.rstrip() for line in sys.stdin])
  if args.mode == "run_default":
    with open(f"{this_dir}/day_{args.day}/input-{args.stage.lower()}.txt", "r") as in_file:
      input_lines = [line.rstrip() for line in in_file.readlines()]
    run_single(int(args.day), args.stage, input_lines)
  if args.mode == "test":
    test_single(int(args.day), args.stage)
  if args.mode == "time":
    time_single(int(args.day), args.stage, [line.rstrip() for line in sys.stdin])
  if args.mode == "time_default":
    with open(f"{this_dir}/day_{args.day}/input-{args.stage.lower()}.txt", "r") as in_file:
      input_lines = [line.rstrip() for line in in_file.readlines()]
    time_single(int(args.day), args.stage, input_lines)

def main_day(day: int):
  argparser = argparse.ArgumentParser()
  argparser.add_argument('mode', choices=['test', 'run', 'time', 'run_default', 'time_default'])
  argparser.add_argument('stage', choices=['A', 'B'])
  args = argparser.parse_args()
  
  if args.mode == "run":
    run_single(day, args.stage, [line.rstrip() for line in sys.stdin])
  if args.mode == "test":
    test_single(day, args.stage)
  if args.mode == "time":
    time_single(day, args.stage, [line.rstrip() for line in sys.stdin])

if __name__ == '__main__':
  main()
