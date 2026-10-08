#!/bin/bash

echo "OSRS Profit Advisor - Quick start"
echo "=================================="
echo ""

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup.sh..."
    bash setup.sh
fi

echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Starting OSRS Profit Advisor..."
echo ""

python run.py
