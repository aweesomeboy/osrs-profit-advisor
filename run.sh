#!/bin/bash

echo "OSRS Profit Advisor - Launcher"
echo "============================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [ ! -f ".venv/bin/activate" ]; then
    echo "[!] Virtual environment not found. Running setup..."
    bash quick-setup.sh
    echo ""
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Verifying PySide6..."
if ! python3 -c "from PySide6.QtWidgets import QApplication" 2>/dev/null; then
    echo "[!] PySide6 not found. Reinstalling..."
    pip install --upgrade PySide6
fi

echo ""
echo "Starting OSRS Profit Advisor..."
echo ""

python run.py
