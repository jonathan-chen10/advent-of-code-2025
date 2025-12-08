#!/bin/bash

ORIG_DIR="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ -z "$1" ]
then
  echo "Usage: new-day.sh <day-number>"
else
  echo "Generating day $1"
  mkdir day_$1/
  cd day_$1
  touch __init__.py
  echo "UNINITIALIZED" > input-a-test.txt
  echo "UNINITIALIZED" > input-a.txt
  echo "UNINITIALIZED" > output-a-test.txt
  ln -s input-a-test.txt input-b-test.txt
  ln -s input-a.txt input-b.txt
  echo "UNINITIALIZED" > output-b-test.txt
  sed "s/main_day(-1) # replace with the current day/main_day($1)/"\
  ../template.py > ./soln.py
fi

cd $ORIG_DIR
