#!/bin/bash
set -e

echo "OSRS Profit Advisor Setup Script"
echo "=================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/7] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo ""
    echo "Install it using:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-full python3-venv python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"

echo ""
echo "[2/7] Checking for python3-full (required on Debian/Ubuntu 12.2+)..."
if command -v apt &> /dev/null; then
    if ! python3 -m ensurepip --version &>/dev/null 2>&1; then
        echo "[!] python3-full not found. Installing..."
        sudo apt update
        sudo apt install -y python3-full python3-venv
        echo "✓ python3-full installed"
    else
        echo "✓ python3-full is available"
    fi
else
    echo "✓ Skipping python3-full check (not on Debian/Ubuntu)"
fi

echo ""
echo "[3/7] Removing old virtual environment if corrupted..."
if [ -d ".venv" ]; then
    if [ ! -f ".venv/bin/python3" ] || [ ! -f ".venv/bin/activate" ]; then
        echo "Virtual environment appears corrupted. Removing..."
        rm -rf .venv
    fi
fi

echo ""
echo "[4/7] Creating fresh virtual environment..."
if [ -d ".venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv .venv --upgrade-deps
    echo "✓ Virtual environment created"
fi

echo ""
echo "[5/7] Activating virtual environment..."
if [ ! -f ".venv/bin/activate" ]; then
    echo "ERROR: Virtual environment activation script not found."
    echo "Try manually:"
    echo "  rm -rf .venv"
    echo "  python3 -m venv .venv"
    exit 1
fi
source .venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "[6/7] Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "[7/7] Initializing database and creating directories..."
mkdir -p data logs

if [ -f "osrs_profit_advisor/database.py" ]; then
    python3 -c "from osrs_profit_advisor.database import initialize_database; db = initialize_database(); print(f'✓ Database: {db}')"
else
    echo "✓ Database initialization skipped (not needed yet)"
fi

echo ""
echo "=================================="
echo "✓ Setup complete!"
echo ""
echo "To run the application:"
echo "  source .venv/bin/activate"
echo "  python run.py"
echo ""
echo "Or use the quick launcher:"
echo "  bash run.sh"
echo ""
echo "To verify everything works:"
echo "  source .venv/bin/activate"
echo "  python -c \"import PySide6; print('✓ PySide6 installed')\""
echo ""
