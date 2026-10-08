#!/bin/bash
set -e

echo "OSRS Profit Advisor - Comprehensive Setup & Build"
echo "=================================================="
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
    echo "  4) Build AppImage (.AppImage file)"
    echo "  5) Build .deb package (Debian/Ubuntu)"
    echo "  6) Install system-wide (/opt)"
    echo "  7) Setup development environment"
    echo "  8) Exit"
    echo ""
    read -p "Select an option (1-8): " choice
case $choice in
    1)
        echo ""
        bash setup.sh
        ;;
    2)
        echo ""
        if [ ! -d ".venv" ]; then
            echo "Virtual environment not found. Running setup.sh first..."
            bash setup.sh
        fi
        source .venv/bin/activate
        python run.py
        ;;
    3)
        echo ""
        if [ ! -d ".venv" ]; then
            echo "Virtual environment not found. Running setup.sh first..."
            bash setup.sh
        fi
        source .venv/bin/activate
        pytest -v
        ;;
    4)
        echo ""
        bash build_appimage.sh
        ;;
    5)
        echo ""
        bash build_deb.sh
        ;;
    6)
        echo ""
        bash install.sh
        ;;
    7)
        echo ""
        bash dev-setup.sh
        ;;
    8)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid option. Please select 1-8."
        show_menu
        ;;
    esac
}

show_menu
