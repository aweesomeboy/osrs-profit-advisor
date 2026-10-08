#!/bin/bash

echo "Making all setup scripts executable..."
chmod +x setup.sh 2>/dev/null || true
chmod +x quick-setup.sh 2>/dev/null || true
chmod +x fix-setup.sh 2>/dev/null || true
chmod +x run.sh 2>/dev/null || true
chmod +x setup-menu.sh 2>/dev/null || true
chmod +x build_appimage.sh 2>/dev/null || true
chmod +x build_deb.sh 2>/dev/null || true
chmod +x install.sh 2>/dev/null || true
chmod +x dev-setup.sh 2>/dev/null || true

echo "✓ All setup scripts are now executable."
echo ""
echo "Quick start options:"
echo ""
echo "1. Fastest setup (recommended):"
echo "   bash quick-setup.sh"
echo ""
echo "2. Run the app after setup:"
echo "   bash run.sh"
echo ""
echo "3. Interactive menu:"
echo "   bash setup-menu.sh"
echo ""
echo "4. Fix corrupted setup:"
echo "   bash fix-setup.sh"
echo ""
