#!/bin/bash

echo "Making all setup scripts executable..."
chmod +x setup.sh
chmod +x build_appimage.sh
chmod +x build_deb.sh
chmod +x install.sh
chmod +x dev-setup.sh
chmod +x run.sh
chmod +x setup-menu.sh

echo "All setup scripts are now executable."
echo ""
echo "To get started, run:"
echo "  bash setup-menu.sh"
echo ""
echo "Or for quick setup:"
echo "  bash setup.sh"
echo ""
