#!/bin/bash

ORIG_DIR="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(pwd)"

for i in {1..12}
do
  SOLN_FILE="$SCRIPT_DIR/day_${i}/soln.py"
  RUNNER_FILE="$SCRIPT_DIR/runner.py"
  if [ -e "$SOLN_FILE" ]; then
    python $RUNNER_FILE test $i A
    python $RUNNER_FILE test $i B
  fi
done
echo "=================================="

cd $ORIG_DIR
