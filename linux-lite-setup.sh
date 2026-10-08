#!/bin/bash
set -e

cd "$HOME/osrs-profit-advisor" || {
  echo "Project folder not found at ~/osrs-profit-advisor"
  echo "Please clone the repo first or move it to your home folder."
  exit 1
}

sudo apt update
sudo apt install -y python3 python3-full python3-venv python3-pip libxkbcommon-x11-0 libdbus-1-3
rm -rf .venv
python3 -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install PySide6 requests PyYAML pytest
python run.py
