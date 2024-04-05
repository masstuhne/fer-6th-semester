#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <folder> <num_of_days>"
    exit 1
fi

directory=$1
if [ ! -d "$directory" ]; then
    echo "Directory: '$directory' does not exist"
    exit 1
fi

if ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Usage: $0 <folder> <num_of_days>"
    echo "--> <num_of_days> must be a whole number"
    exit 1
fi

total_words=0

files=$(find "$1" -type f -mtime "-$2")
for file in $files; do
    word_count=$(wc -w <"$file")
    echo "$file ........ $word_count rijeci"
    total_words=$((total_words + word_count))
done

echo "------------------------------"
echo "Ukupno: $total_words rijeci"
