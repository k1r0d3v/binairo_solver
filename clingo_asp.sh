#!/bin/bash
n=0
clingo -c size=$1 0 asp.lp | grep '[a-zA-Z]([0-9]' | 
while read line
do
    n=$((n+1))
    echo "Result: $n"
    ./asp -p $1 "$line"
    echo ""
done
