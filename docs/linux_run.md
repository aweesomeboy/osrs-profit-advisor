# Linux run guide

## Overview

This project is designed for Linux desktops and uses a virtual environment for dependencies.

## Requirements

- Python 3.10+
- Git
- pip

## Quick start

```bash
git clone https://github.com/aweesomeboy/osrs-profit-advisor.git
cd osrs-profit-advisor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Troubleshooting

- If PySide6 fails to install, ensure Qt dependencies are available on your Linux system.
- If the app cannot create the database, make sure the project folder is writable.
- If the OSRS Wiki API blocks the request, verify your User-Agent and internet connectivity.
