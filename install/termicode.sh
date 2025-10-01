#!/usr/bin/env bash
# Terminal Coding Assistant - Quick launcher for Linux/Mac

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to script directory and run main.py
cd "$SCRIPT_DIR"
python3 main.py
