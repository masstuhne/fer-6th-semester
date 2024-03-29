#!/bin/bash

#---------------------------------------

if [ $# -ne 1 ]; then
    echo "Usage: $0 <name_of_the_folder>"
    exit 1
fi

directory=$1
if [ ! -d "$directory" ]; then
    echo "Directory: '$directory' does not exist"
    exit 1
fi

log_files=$(find "$directory" -type f -name "*_log*-02-*.txt")
for file in $log_files; do
    date=$(basename "$file" | grep -o -E "[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}")
    formated_date=$(date -d "$date" +"%d-%m-%Y")
    echo "datum: $formated_date"
    echo "--------------------------------------------------"

    awk '{print $6 " " $7 " " $8}' "$file" | sort | uniq -c | sort -n -r
    echo
done

#---------------------------------------
