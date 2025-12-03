#!/bin/bash

ORIG_DIR="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(pwd)"

echo "============="
echo "LINES OF CODE"
for i in {1..12}
do
  SOLN_FILE="$SCRIPT_DIR/day_${i}/soln.py"
  if [ -e "$SOLN_FILE" ]; then
    echo "Day $i    $(wc -l < $SOLN_FILE | tr -d '[:space:]')"
  else
    break
  fi
done
echo "============="

cd $ORIG_DIR
