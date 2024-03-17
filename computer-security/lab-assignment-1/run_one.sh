#!/bin/bash

PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Run scenario: Custom

echo
echo -e "${PURPLE}---------------------------------${NC}"
echo -e "${PURPLE}Run scenario: $1${NC}"
echo

python3 main.py "$@"