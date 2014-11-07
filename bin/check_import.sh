#!/usr/bin/env bash
BASE=/home/websites/mhmob-admin/bin/new_bin/bin
PYTHON=/usr/bin/python

result1=$(mktemp)
result2=$(mktemp)

cd $BASE
$PYTHON $BASE/check_import.py $1 > result1 2&>1
$PYTHON $BASE/check_import.py $1 "002" > result2 2&>1

diff result1 result2

rm -f result1 result2
