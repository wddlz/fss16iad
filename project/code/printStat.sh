#!/bin/bash

while [ $# -gt 1 ]
do
key="$1"

case $key in
    -u|--uuid)
    UUID="$2"
    shift # past argument
    ;;

esac
done

echo $UUID

for i in stats/*$UUID*.txt; do # Whitespace-safe but not recursive.
    	echo "\n\nStatistics for $i\n===================================================================================="
	cat "$i"|python stats/stats.py
done
