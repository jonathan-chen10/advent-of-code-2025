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
  if [ -e "$SOLN_FILE" ]; then
    start_a=$(gdate +%s.%N)
    _res=$(python $SOLN_FILE run A < "$SCRIPT_DIR/day_${i}/input-a.txt")
    end_a=$(gdate +%s.%N)
    start_b=$(gdate +%s.%N)
    _res=$(python $SOLN_FILE run B < "$SCRIPT_DIR/day_${i}/input-b.txt")
    end_b=$(gdate +%s.%N)
    wc -l < $SOLN_FILE | tr -d '[:space:]' \
    | xargs -I {} printf "Day %-2s    %3s  %8.f  %8.f\n" $i {} "\
    "$(echo "$end_a - $start_a" | bc) $(echo "$end_b - $start_b" | bc)
  else
    echo "Day $i"
  fi
done
echo "=================================="

cd $ORIG_DIR
