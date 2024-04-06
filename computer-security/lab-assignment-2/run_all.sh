#!/bin/bash

PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Run scenario: Initialize, Add, Login, Change Password, Wrong Login

if [ -f "user_database_final.db" ]; then
  rm -f "user_database_final.db"
fi

echo
echo -e "${PURPLE}---------------------------------${NC}"
echo -e "${PURPLE}Run scenario: Initialize, Add, Login, Change Password, Wrong Login${NC}"
echo

echo "Task: Initialize database"
python3 database_commands.py

echo "Task: Add user with username masstuhne"
echo -e "Test123-\nTest123-\n" | python3 admin_console.py add masstuhne

echo "Task: Login with username masstuhne"
echo -e "Test123-\n" | python3 user_login.py masstuhne

echo "Task: Update password for username masstuhne"
echo -e "Masstuhne123-\nMasstuhne123-\n" | python3 admin_console.py passwd masstuhne

echo "Task: Login with username masstuhne --> Wrong Password"
echo -e "Test123-\n" | python3 user_login.py masstuhne

# Run scenario: Force Password Change, Login

echo
echo -e "${PURPLE}---------------------------------${NC}"
echo -e "${PURPLE}Force Password Change, Login${NC}"
echo

echo "Task: Force password change for username masstuhne"
python3 admin_console.py forcepass masstuhne

echo "Task: Login with username masstuhne --> Force Password Change"
echo -e "Masstuhne123-\nTest123-\nTest123-\n" | python3 user_login.py masstuhne

# Run scenario: Delete, Login

echo
echo -e "${PURPLE}---------------------------------${NC}"
echo -e "${PURPLE}Run scenario: Delete, Login${NC}"
echo

echo "Task: Delete user with username masstuhne"
python3 admin_console.py del masstuhne

echo "Task: Login with username masstuhne"
echo -e "Test123-\n" | python3 user_login.py masstuhne
