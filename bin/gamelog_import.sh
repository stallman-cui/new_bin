#!/usr/bin/env bash
BASE=/home/mhgame
GAME_BASE=$BASE/games
BIN_BASE=$BASE/data_analysis/bin
PYTHON=/usr/bin/python

cd $BIN_BASE

echo $(date  +'[%Y-%m-%d : %H:%M:%S]') " gamelog import start ..."

hosts=$($PYTHON $BIN_BASE/host.py)

exec_command='t=$(expr $(date +%s) / 300 - 1);t=$(date --date @$(expr $t \* 300) +%Y%m%d%H%M); for g in /home/mhgame/games/*; do find $g/log/gamelog -name mh_$t.log | xargs sed -e "s/^/$(basename $g)\t/"; done 2>/dev/null'

for host in $hosts; do
	ssh -o "StrictHostKeyChecking no" $host $exec_command 2>/dev/null | $BIN_BASE/gamelog_import.py
done

echo $(date  +'[%Y-%m-%d : %H:%M:%S]') " gamelog import done ..."
