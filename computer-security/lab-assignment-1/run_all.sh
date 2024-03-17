#!/bin/bash

# Run scenario: Initialize, Add, Get, Remove, Get

echo
echo "---------------------------------"
echo

echo "Task: Initialize password manager"
python3 main.py init master_password

echo "Task: Add password for fer.hr"
python3 main.py put master_password fer.hr fer_password

echo "Task: Get password for fer.hr"
python3 main.py get master_password fer.hr

echo "Task: Remove password for fer.hr"
python3 main.py remove master_password fer.hr

echo "Task: Get password for fer.hr"
python3 main.py get master_password fer.hr

# Run scenario: Add, Get, Update, Get

echo
echo "---------------------------------"
echo

echo "Task: Add password for fer.hr"
python3 main.py put master_password fer.hr fer_password

echo "Task: Get password for fer.hr"
python3 main.py get master_password fer.hr

echo "Task: Update password for fer.hr"
python3 main.py put master_password fer.hr fer_password_new

echo "Task: Get password for fer.hr"
python3 main.py get master_password fer.hr

# Run scenario: Add, Get, Get, Remove, Get

echo
echo "---------------------------------"
echo

echo "Task: Add password for example.com"
python3 main.py put master_password example.com example_password

echo "Task: Get password for example.com"
python3 main.py get master_password example.com

echo "Task: Get password for fer.hr"
python3 main.py get master_password fer.hr

echo "Task: Remove password for fer.hr"
python3 main.py remove master_password fer.hr

echo "Task: Get password for example.com"
python3 main.py get master_password example.com

# Run scenario: Get, Put, Remove --> Wrong Master Password

echo
echo "---------------------------------"
echo

echo "Task: Get password for fer.hr --> wrong master password"
python3 main.py get master_password_wrong fer.hr

echo "Task: Put password for fer.hr --> wrong master password"
python3 main.py put master_password_wrong fer.hr password

echo "Task: Remove password for fer.hr --> wrong master password"
python3 main.py remove master_password_wrong fer.hr

# Run scenario: Get

echo
echo "---------------------------------"
echo

echo "Task: Get password for example.com"
python3 main.py get master_password example.com

# Run scenario: Initialize, Get

echo
echo "---------------------------------"
echo

echo "Task: Initialize password manager"
python3 main.py init master_password

echo "Task: Get password for example.com"
python3 main.py get master_password example.com







