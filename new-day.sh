#!/bin/bash

ORIG_DIR="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ -z "$1" ]
then
  echo "Usage: new-day.sh <day-number>"
else
  new_dir=day_$(printf "%02d" $1)
  if [ -e "$new_dir" ]
  then
    echo "Directory $new_dir already exists!"
  else
    echo "Generating day $1"
    mkdir $new_dir/
    cd $new_dir
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
fi

cd $ORIG_DIR
