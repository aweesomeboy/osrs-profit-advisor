#!/bin/bash
set -e

echo "OSRS Profit Advisor - Interactive Setup"
echo "========================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

show_menu() {
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "  1) Setup for running locally (recommended for first time)"
    echo "  2) Run the application"
    echo "  3) Run tests"
    echo "  4) Fix corrupted setup"
    echo "  5) Build AppImage (.AppImage file)"
    echo "  6) Build .deb package (Debian/Ubuntu)"
    echo "  7) Exit"
    echo ""
    read -p "Select an option (1-7): " choice

case $choice in
    1)
        echo ""
        bash quick-setup.sh
        show_menu
        ;;
    2)
        echo ""
        bash run.sh
        ;;
    3)
        echo ""
        if [ ! -d ".venv" ]; then
            echo "Virtual environment not found. Running setup first..."
            bash quick-setup.sh
        fi
        source .venv/bin/activate
        pytest -v
        show_menu
        ;;
    4)
        echo ""
        bash fix-setup.sh
        show_menu
        ;;
    5)
        echo ""
        bash build_appimage.sh
        show_menu
        ;;
    6)
        echo ""
        bash build_deb.sh
        show_menu
        ;;
    7)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid option. Please select 1-7."
        show_menu
        ;;
    esac
}

show_menu
