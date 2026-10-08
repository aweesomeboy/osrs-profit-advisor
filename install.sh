#!/bin/bash
set -e

echo "Installing OSRS Profit Advisor from source"
echo "==========================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/4] Running setup.sh..."
bash setup.sh

echo ""
echo "[2/4] Creating /opt installation directory..."
INSTALL_DIR="/opt/osrs-profit-advisor"

if [ -d "$INSTALL_DIR" ]; then
    echo "Removing existing installation at $INSTALL_DIR..."
    sudo rm -rf "$INSTALL_DIR"
fi

sudo mkdir -p "$INSTALL_DIR"
sudo cp -r .venv osrs_profit_advisor data docs tests requirements.txt run.py "$INSTALL_DIR/"
sudo chmod 755 "$INSTALL_DIR"
sudo chmod 755 "$INSTALL_DIR/run.py"

echo ""
echo "[3/4] Creating launcher script..."
sudo tee /usr/local/bin/osrs-profit-advisor > /dev/null << 'EOF'
#!/bin/bash
cd /opt/osrs-profit-advisor
source .venv/bin/activate
python run.py
EOF
sudo chmod 755 /usr/local/bin/osrs-profit-advisor

echo ""
echo "[4/4] Creating desktop entry..."
sudo tee /usr/share/applications/osrs-profit-advisor.desktop > /dev/null << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=OSRS Profit Advisor
Comment=Grand Exchange price tracker and profit calculator for Old School RuneScape
Exec=osrs-profit-advisor
Icon=application-x-executable
Categories=Utility;Finance;
Terminal=false
EOF

echo ""
echo "==========================================="
echo "Installation complete!"
echo ""
echo "You can now run the application with:"
echo "  osrs-profit-advisor"
echo ""
echo "Or from the applications menu (look for OSRS Profit Advisor)."
echo ""
echo "Data is stored at:"
echo "  /opt/osrs-profit-advisor/data/"
echo ""
echo "To uninstall:"
echo "  sudo rm -rf /opt/osrs-profit-advisor"
echo "  sudo rm /usr/local/bin/osrs-profit-advisor"
echo "  sudo rm /usr/share/applications/osrs-profit-advisor.desktop"
echo ""
