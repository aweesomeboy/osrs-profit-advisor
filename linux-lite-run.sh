#!/bin/bash
set -e

cd "$HOME/osrs-profit-advisor" || {
  echo "Project folder not found at ~/osrs-profit-advisor"
  echo "Please clone the repo first or move it to your home folder."
  exit 1
}

source .venv/bin/activate
python run.py
