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

declare -A grouped_photos
photo_files=$(find "$directory" -type f -name "*.jpg" | sort)
for photo in $photo_files; do
    year_month=$(basename "$photo" | grep -o -E "[[:digit:]]{8}_[[:digit:]]{4}" | sed -E "s/([[:digit:]]{4})([[:digit:]]{2})([[:digit:]]{2})_([[:digit:]]{4})/\1-\2/")
    grouped_photos["$year_month"]+="$(basename "$photo") "
done

sorted_year_month=$(printf '%s\n' "${!grouped_photos[@]}" | sort)

for year_month in $sorted_year_month; do
    echo "$(date -d "$year_month"-01 +"%m-%Y") :"
    echo "----------"
    i=1
    sorted_photos=$(echo "${grouped_photos["$year_month"]}" | tr " " "\n")
    for photo in $sorted_photos; do
        echo "   $i. $photo"
        ((i++))
    done
    num_photos=$(echo "$sorted_photos" | wc -w)
    echo "--- Ukupno: $num_photos slika ---"
done

#---------------------------------------
