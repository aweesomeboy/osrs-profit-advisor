#!/bin/bash
set -e

echo "OSRS Profit Advisor Setup Script"
echo "=================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/6] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.10 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Found Python $PYTHON_VERSION"

echo ""
echo "[2/6] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv .venv
    echo "Virtual environment created at .venv/"
fi

echo ""
echo "[3/6] Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "[4/6] Upgrading pip and installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "[5/6] Initializing database..."
python3 -c "from osrs_profit_advisor.database import initialize_database; db = initialize_database(); print(f'Database initialized at: {db}')"

echo ""
echo "[6/6] Creating data directories..."
mkdir -p data logs
touch data/.gitkeep logs/.gitkeep

echo ""
echo "=================================="
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python run.py"
echo ""
echo "To run tests:"
echo "  pytest -v"
echo ""
echo "To build AppImage:"
echo "  bash build_appimage.sh"
echo ""
