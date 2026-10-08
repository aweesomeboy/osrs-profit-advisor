#!/bin/bash

# OSRS Profit Advisor - Startup Script

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "=========================================="
echo "OSRS Profit Advisor"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r "$PROJECT_DIR/requirements.txt"

echo ""
echo "=========================================="
echo "Starting OSRS Profit Advisor"
echo "=========================================="
echo ""
echo "✓ Backend will start in a moment..."
echo "✓ Application will be available at:"
echo ""
echo "    http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""
echo "=========================================="
echo ""

cd "$PROJECT_DIR"
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
