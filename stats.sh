#!/bin/bash

ORIG_DIR="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(pwd)"

echo "=================================="
echo "            STATISTICS            "
echo " DAY      LOC    SECS(A)   SECS(B)"
echo "=================================="
echo "TEMPLATE   $(wc -l < "$SCRIPT_DIR/template.py" | tr -d '[:space:]')"
for i in {1..12}
do
  SOLN_FILE="$SCRIPT_DIR/day_${i}/soln.py"
  RUNNER_FILE="$SCRIPT_DIR/runner.py"
  if [ -e "$SOLN_FILE" ]; then
    time_a=$(python $RUNNER_FILE time-default $i A)
    time_b=$(python $RUNNER_FILE time-default $i B)
    wc -l < $SOLN_FILE | tr -d '[:space:]' \
    | xargs -I {} printf "Day %-2s    %3s  %8.3f  %8.3f\n" $i {} $time_a $time_b
  else
    echo "Day $i"
  fi
done
echo "=================================="

cd $ORIG_DIR
