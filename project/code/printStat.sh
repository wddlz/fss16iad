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

purchase="purchase_$UUID\.txt"
cat stats/*purchase*$UUID* >$purchase


utility="utility_$UUID\.txt"
cat stats/*utility*$UUID* >$utility

time="time_$UUID\.txt"
cat stats/*time*$UUID* >$time
for i in *$UUID*.txt; do # Whitespace-safe but not recursive.
    	echo "\n\nStatistics for $i\n===================================================================================="
	cat "$i"|python stats/stats.py
done
