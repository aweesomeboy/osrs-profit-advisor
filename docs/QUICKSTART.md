# OSRS Profit Advisor Setup Guide - Linux Lite & Ubuntu

## TL;DR (Fastest way)

```bash
cd ~/osrs-profit-advisor
bash quick-setup.sh
bash run.sh
```

That's it. The app should start.

## What if it doesn't work?

Try the fix script:

```bash
bash fix-setup.sh
```

If that still doesn't work, see `docs/TROUBLESHOOTING.md` for detailed solutions.

## Step-by-step setup

### 1. Install system dependencies

**Linux Lite / Ubuntu / Debian:**

```bash
sudo apt update
sudo apt install -y python3 python3-full python3-venv python3-pip \
  libxkbcommon-x11-0 libdbus-1-3 libfontconfig1 libfreetype6
```

**Fedora / RHEL:**

```bash
sudo dnf install -y python3 python3-pip libxkbcommon libdbus fontconfig freetype
```

### 2. Clone or navigate to the project

```bash
git clone https://github.com/aweesomeboy/osrs-profit-advisor.git
cd osrs-profit-advisor
```

### 3. Run the quick setup

```bash
bash quick-setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Initialize the database
- Verify everything works

### 4. Run the application

```bash
bash run.sh
```

Or manually:

```bash
source .venv/bin/activate
python run.py
```

## Available commands

| Command | Purpose |
|---------|----------|
| `bash quick-setup.sh` | Fast setup (recommended) |
| `bash setup.sh` | Detailed setup |
| `bash run.sh` | Launch the app |
| `bash fix-setup.sh` | Fix corrupted setup |
| `bash setup-menu.sh` | Interactive menu |
| `bash build_appimage.sh` | Build standalone AppImage |
| `bash build_deb.sh` | Build .deb package |

## Running the app

### After setup

```bash
bash run.sh
```

### Or manually activate venv

```bash
source .venv/bin/activate
python run.py
```

## Building for distribution

### AppImage (portable)

```bash
bash build_appimage.sh
./OSRSProfitAdvisor-x86_64.AppImage
```

### .deb package (Ubuntu/Debian)

```bash
bash build_deb.sh
sudo apt install ./osrs-profit-advisor_0.1.0_amd64.deb
osrs-profit-advisor
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues and solutions.

Quick fixes:

```bash
# Fix PEP 668 issues
sudo apt install python3-full
rm -rf .venv
python3 -m venv .venv --upgrade-deps

# Reinstall dependencies
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## First use

1. Launch the app
2. Initial sync of price data happens automatically (30-60 seconds)
3. Use the tabs to explore:
   - **Dashboard**: Overview
   - **Item Search**: Browse items
   - **Recipes**: Manage and view recipes
   - **Price Forecast**: See trends
   - **Settings**: Configure the app

## Need help?

- Check `docs/TROUBLESHOOTING.md`
- Check `docs/SETUP.md` for detailed docs
- Run tests: `pytest -v`
- Check logs in `logs/` folder (after first run)

## Uninstall

```bash
rm -rf ~/.osrs-profit-advisor data logs .venv
```
