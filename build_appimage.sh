#!/bin/bash
set -e

echo "Building OSRS Profit Advisor AppImage"
echo "======================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/5] Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required."
    exit 1
fi

if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[!] PyInstaller not found. Installing..."
    source .venv/bin/activate 2>/dev/null || {
        echo "ERROR: Virtual environment not found. Run setup.sh first."
        exit 1
    }
    pip install PyInstaller
else
    echo "PyInstaller found."
fi

echo ""
echo "[2/5] Cleaning previous builds..."
rm -rf build dist *.spec

echo ""
echo "[3/5] Building standalone executable with PyInstaller..."
PYINSTALLER_ARGS=(
    "--name=OSRSProfitAdvisor"
    "--onefile"
    "--windowed"
    "--icon=docs/osrs-profit-advisor.png"
    "--add-data=data:data"
    "--add-data=docs:docs"
    "--hidden-import=PySide6"
    "--hidden-import=requests"
    "--hidden-import=yaml"
    "run.py"
)

pyinstaller "${PYINSTALLER_ARGS[@]}"

echo ""
echo "[4/5] Creating AppImage structure..."
BUILD_DIR="OSRSProfitAdvisor.AppDir"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/usr/bin" "$BUILD_DIR/usr/lib" "$BUILD_DIR/usr/share/applications" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

cp dist/OSRSProfitAdvisor "$BUILD_DIR/usr/bin/"

cat > "$BUILD_DIR/usr/share/applications/osrs-profit-advisor.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=OSRS Profit Advisor
Comment=Grand Exchange price tracker and profit calculator for Old School RuneScape
Exec=OSRSProfitAdvisor
Icon=osrs-profit-advisor
Categories=Utility;Finance;
Terminal=false
EOF

echo ""
echo "[5/5] Checking for appimagetool..."
if command -v appimagetool &> /dev/null; then
    echo "Building AppImage with appimagetool..."
    appimagetool "$BUILD_DIR" "OSRSProfitAdvisor-x86_64.AppImage" || {
        echo "WARNING: appimagetool failed. Check your environment."
        echo "The application is ready at: $BUILD_DIR/usr/bin/OSRSProfitAdvisor"
    }
    chmod +x OSRSProfitAdvisor-x86_64.AppImage
    echo "AppImage created: OSRSProfitAdvisor-x86_64.AppImage"
else
    echo "appimagetool not found. Creating executable bundle instead..."
    echo "The application is ready at: $BUILD_DIR/usr/bin/OSRSProfitAdvisor"
    echo ""
    echo "To install appimagetool on Ubuntu/Debian:"
    echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    echo "  chmod +x appimagetool-x86_64.AppImage"
    echo "  sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
fi

echo ""
echo "======================================"
echo "Build complete!"
echo ""
echo "To run the application:"
if [ -f "OSRSProfitAdvisor-x86_64.AppImage" ]; then
    echo "  ./OSRSProfitAdvisor-x86_64.AppImage"
else
    echo "  $BUILD_DIR/usr/bin/OSRSProfitAdvisor"
fi
echo ""
