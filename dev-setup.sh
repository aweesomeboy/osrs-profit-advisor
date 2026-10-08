#!/bin/bash
set -e

echo "OSRS Profit Advisor - Development Setup"
echo "========================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/4] Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo ""
echo "[2/4] Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "[3/4] Installing dependencies (including dev tools)..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install PyInstaller black flake8 isort

echo ""
echo "[4/4] Setting up git hooks for formatting..."
if [ -d ".git" ]; then
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running code formatters..."
black osrs_profit_advisor tests
isort osrs_profit_advisor tests
flake8 osrs_profit_advisor tests || true
EOF
    chmod +x .git/hooks/pre-commit
    echo "Git hooks installed."
fi

echo ""
echo "========================================="
echo "Development setup complete!"
echo ""
echo "Available commands:"
echo "  python run.py                 - Run the app"
echo "  pytest -v                     - Run tests"
echo "  pytest -v --cov               - Run tests with coverage"
echo "  black osrs_profit_advisor     - Format code"
echo "  flake8 osrs_profit_advisor    - Lint code"
echo "  bash build_appimage.sh        - Build AppImage"
echo "  bash build_deb.sh             - Build .deb package"
echo ""
