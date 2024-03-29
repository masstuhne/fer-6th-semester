#!/bin/bash

#---------------------------------------

if [ $# -ne 2 ]; then
    echo "Usage: $0 <name_of_the_folder_1> <name_of_the_folder_2>"
    exit 1
fi

if [ ! -d "$1" ] || [ ! -d "$2" ]; then
    echo "Directory $1 or $2 does not exist"
    exit 1
fi

directory_1=$1
directory_2=$2

for file in "$directory_1"*; do
    if [ -f "$file" ] && [ "$file" -nt "$directory_2/$(basename "$file")" ]; then
        echo "$file --> $directory_2"
    fi
done

for file in "$directory_2"*; do
    if [ -f "$file" ] && [ "$file" -nt "$directory_1/$(basename "$file")" ]; then
        echo "$file --> $directory_1"
    fi
done

#---------------------------------------
