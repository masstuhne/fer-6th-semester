#!/bin/bash

#---------------------------------------

grep -i -E 'banana|jabuka|jagoda|dinja|lubenica' ./namirnice.txt

#---------------------------------------

grep -v -i -E 'banana|jabuka|jagoda|dinja|lubenica' ./namirnice.txt

#---------------------------------------

grep -r -E '\b.+(A-Z){3}[0-9]{6}.+\b' ~/projekti/

#---------------------------------------

find ./ -type f -mtime +7 -mtime -14 -ls

#---------------------------------------

# for i in {1..15}; do
for i in $(seq 1 15); do
    echo $i
done

#---------------------------------------

kraj=15
for i in $(seq 1 $kraj); do
    echo $i
done

#---------------------------------------

# This is not supported, first nor second example:
# for i in {1..$kraj}; do
for i in $(1..$kraj); do
    echo $i
done

#---------------------------------------
