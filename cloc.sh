#!/bin/bash

ORIG_DIR="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(pwd)"

echo "============="
echo "LINES OF CODE"
echo "============="
echo "TEMPLATE   $(wc -l < "$SCRIPT_DIR/template.py" | tr -d '[:space:]')"
for i in {1..12}
do
  SOLN_FILE="$SCRIPT_DIR/day_${i}/soln.py"
  if [ -e "$SOLN_FILE" ]; then
    wc -l < $SOLN_FILE | tr -d '[:space:]' | xargs printf "Day %-2s    %3s\n" $i
  else
    echo "Day $i"
  fi
done
echo "============="

cd $ORIG_DIR
