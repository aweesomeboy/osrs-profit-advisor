#!/bin/bash

echo "OSRS Profit Advisor - All-in-one Setup"
echo "====================================="
echo ""
echo "This script will prepare everything you need to run the app."
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/5] Checking system requirements..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo ""
    echo "Install it using:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

echo ""
echo "[2/5] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "[3/5] Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip -q
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "[4/5] Initializing database..."
python3 -c "from osrs_profit_advisor.database import initialize_database; db = initialize_database(); print(f'✓ Database: {db}')"

echo ""
echo "[5/5] Creating directories..."
mkdir -p data logs
echo "✓ Directories created"

echo ""
echo "====================================="
echo "✓ Setup complete!"
echo ""
echo "To run the app:"
echo "  source .venv/bin/activate"
echo "  python run.py"
echo ""
echo "Or use the launcher:"
echo "  bash run.sh"
echo ""
