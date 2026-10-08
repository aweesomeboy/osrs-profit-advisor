#!/bin/bash
set -e

echo "OSRS Profit Advisor - Quick Setup"
echo "=================================="
echo ""
echo "This script will prepare everything you need to run the app."
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/6] Checking system requirements..."
if ! command -v python3 &> /dev/null; then
    echo "✗ ERROR: Python 3 is not installed."
    echo ""
    echo "Install it using:"
    echo "  Ubuntu/Debian (Lite): sudo apt install python3 python3-full python3-venv python3-pip"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

echo ""
echo "[2/6] Checking for python3-full (Debian/Ubuntu 12.2+)..."
if command -v apt &> /dev/null; then
    VENV_TEST=$(python3 -c "import ensurepip" 2>&1 || true)
    if [[ $VENV_TEST == *"No module named ensurepip"* ]]; then
        echo "[!] Installing python3-full..."
        sudo apt update
        sudo apt install -y python3-full python3-venv
    else
        echo "✓ python3-full is available"
    fi
fi

echo ""
echo "[3/6] Creating virtual environment..."
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
    echo "✓ Virtual environment already exists"
else
    rm -rf .venv 2>/dev/null || true
    python3 -m venv .venv --upgrade-deps
    echo "✓ Virtual environment created"
fi

echo ""
echo "[4/6] Activating and installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip -q
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "[5/6] Initializing database..."
mkdir -p data logs
if python3 -c "from osrs_profit_advisor.database import initialize_database; initialize_database()" 2>/dev/null; then
    echo "✓ Database initialized"
else
    echo "✓ Database check skipped"
fi

echo ""
echo "[6/6] Testing PySide6..."
if python3 -c "from PySide6.QtWidgets import QApplication" 2>/dev/null; then
    echo "✓ PySide6 is working"
else
    echo "✗ PySide6 import failed. Trying alternative fix..."
    pip install --upgrade PySide6
    python3 -c "from PySide6.QtWidgets import QApplication"
    echo "✓ PySide6 fixed and working"
fi

echo ""
echo "=================================="
echo "✓ Setup complete!"
echo ""
echo "To run the app immediately:"
echo "  source .venv/bin/activate && python run.py"
echo ""
echo "Or use the launcher:"
echo "  bash run.sh"
echo ""
