#!/bin/bash
set -e

echo "Checking and fixing setup..."
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "Step 1: Removing corrupted .venv if present..."
if [ -d ".venv" ]; then
    rm -rf .venv
    echo "✓ Old virtual environment removed"
fi

echo ""
echo "Step 2: Running setup..."
bash setup.sh

echo ""
echo "Step 3: Testing the app..."
source .venv/bin/activate

echo "  - Checking PySide6..."
if python3 -c "from PySide6.QtWidgets import QApplication; print('  ✓ PySide6 OK')" 2>/dev/null; then
    :  # Success, continue
else
    echo "  - Reinstalling PySide6..."
    pip install --upgrade PySide6
    python3 -c "from PySide6.QtWidgets import QApplication; print('  ✓ PySide6 OK')"
fi

echo "  - Checking other imports..."
python3 -c "from osrs_profit_advisor import calculations; print('  ✓ Calculations OK')"
python3 -c "from osrs_profit_advisor.database import initialize_database; print('  ✓ Database OK')"

echo ""
echo "✓ All checks passed!"
echo ""
echo "You can now run:"
echo "  bash run.sh"
echo ""
