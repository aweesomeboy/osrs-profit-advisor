#!/bin/bash
set -e

echo "Building .deb package for OSRS Profit Advisor"
echo "=============================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

VERSION="0.1.0"
PKG_NAME="osrs-profit-advisor"
ARCH="amd64"

echo "[1/5] Checking dependencies..."
if ! command -v dpkg &> /dev/null; then
    echo "ERROR: dpkg is required. This script only works on Debian/Ubuntu."
    exit 1
fi

echo "[2/5] Building PyInstaller executable..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Installing PyInstaller..."
    source .venv/bin/activate 2>/dev/null || {
        echo "ERROR: Virtual environment not found. Run setup.sh first."
        exit 1
    }
    pip install PyInstaller
fi

rm -rf build dist
pyinstaller \
    --name=osrs-profit-advisor \
    --onefile \
    --windowed \
    --add-data=data:data \
    --hidden-import=PySide6 \
    --hidden-import=requests \
    --hidden-import=yaml \
    run.py

echo ""
echo "[3/5] Creating .deb package structure..."
DEB_BUILD="$PROJECT_DIR/deb_build"
rm -rf "$DEB_BUILD"
mkdir -p "$DEB_BUILD/DEBIAN"
mkdir -p "$DEB_BUILD/usr/bin"
mkdir -p "$DEB_BUILD/usr/share/applications"
mkdir -p "$DEB_BUILD/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$DEB_BUILD/usr/share/doc/$PKG_NAME"

cp dist/osrs-profit-advisor "$DEB_BUILD/usr/bin/"
chmod 755 "$DEB_BUILD/usr/bin/osrs-profit-advisor"

cat > "$DEB_BUILD/usr/share/applications/osrs-profit-advisor.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=OSRS Profit Advisor
Comment=Grand Exchange price tracker and profit calculator for Old School RuneScape
Exec=osrs-profit-advisor
Icon=osrs-profit-advisor
Categories=Utility;Finance;
Terminal=false
EOF

cat > "$DEB_BUILD/DEBIAN/control" << EOF
Package: $PKG_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: OSRS Profit Advisor Contributors <osrs-profit-advisor@example.com>
Description: Grand Exchange price tracker and profit calculator for Old School RuneScape
 OSRS Profit Advisor is a Linux desktop application that tracks Grand Exchange prices,
 analyzes recipe profitability, and forecasts short-term market movements.
 .
 Features:
  * Live price tracking from the OSRS Wiki API
  * Recipe management and profit calculations
  * Price history and trend forecasting
  * Local SQLite database for offline analysis
Depends: libqt6core6, libqt6gui6, libqt6widgets6, python3 (>= 3.10)
EOF

cat > "$DEB_BUILD/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e
if command -v update-desktop-database > /dev/null 2>&1; then
  update-desktop-database -q /usr/share/applications
fi
if command -v update-icon-caches > /dev/null 2>&1; then
  update-icon-caches /usr/share/icons/hicolor
fi
EOF
chmod 755 "$DEB_BUILD/DEBIAN/postinst"

echo ""
echo "[4/5] Building package..."
dpkg-deb --build "$DEB_BUILD" "${PKG_NAME}_${VERSION}_${ARCH}.deb"

echo ""
echo "[5/5] Cleaning up..."
rm -rf "$DEB_BUILD" dist build

echo ""
echo "=============================================="
echo "Package build complete!"
echo ""
echo "To install the .deb package:"
echo "  sudo dpkg -i ${PKG_NAME}_${VERSION}_${ARCH}.deb"
echo ""
echo "Or install and resolve dependencies:"
echo "  sudo apt install ./${PKG_NAME}_${VERSION}_${ARCH}.deb"
echo ""
echo "After installation, run:"
echo "  osrs-profit-advisor"
echo ""
