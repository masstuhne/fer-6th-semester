#!/bin/bash

#---------------------------------------

if [ $# -ne 2 ]; then
    echo "Usage: $0 <name_of_the_folder> <regex_of_the_file>"
    exit 1
fi

echo "Directory: $1"
echo "File: $2"

total_lines=0
files=$(find "$1" -type f -name "$2")
for file in $files; do
    lines=$(wc -l <"$file")
    total_lines=$((total_lines + lines))
done

echo "Total number of lines: $total_lines"

#---------------------------------------
