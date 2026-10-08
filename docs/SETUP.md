# OSRS Profit Advisor Setup & Run Guide

## Quick Start (Recommended)

### Option 1: Use the interactive setup menu

```bash
bash setup-menu.sh
```

This will show you options to:
- Setup the application
- Run it locally
- Build AppImage or .deb packages
- Setup development environment

### Option 2: Manual setup

```bash
bash setup.sh
source .venv/bin/activate
python run.py
```

### Option 3: Quick run script

```bash
bash run.sh
```

## What the setup scripts do

### `setup.sh` - Basic setup
- Checks Python 3 installation
- Creates a Python virtual environment
- Installs all dependencies
- Initializes the SQLite database
- Creates data and logs directories

**Use this if:** You want to run the app locally.

### `run.sh` - Quick launcher
- Activates the virtual environment
- Runs the app immediately

**Use this if:** You've already run `setup.sh` and just want to launch the app.

### `build_appimage.sh` - Create AppImage
- Builds a standalone .AppImage executable
- Works on most Linux distributions
- No installation needed - just run it
- Requires `appimagetool` (automatically checked)

**Use this if:** You want a portable, self-contained app.

### `build_deb.sh` - Create .deb package
- Builds a Debian/Ubuntu .deb package
- Can be installed system-wide with `apt`
- Creates menu entry automatically

**Use this if:** You use Debian/Ubuntu and want proper package management.

### `install.sh` - Install system-wide
- Installs to `/opt/osrs-profit-advisor`
- Creates launcher in `/usr/local/bin/`
- Adds desktop menu entry
- Requires `sudo`

**Use this if:** You want the app available for all users on your system.

### `dev-setup.sh` - Development setup
- Installs dev tools (PyInstaller, black, flake8, isort)
- Sets up git hooks for code formatting
- Enables building AppImage/deb locally

**Use this if:** You want to contribute or build packages.

### `setup-menu.sh` - Interactive menu
- Shows all available options
- Lets you choose what to do
- Recommended for first-time users

## System Requirements

- **Linux** (Ubuntu 20.04+, Debian 11+, Fedora 35+, or similar)
- **Python 3.10+** with pip and venv
- **Qt 6** libraries (automatically handled via pip/PySide6)
- **Internet connection** (for API and pip packages)

### Install system dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-venv python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

## Running the application

### After setup

```bash
source .venv/bin/activate
python run.py
```

Or simply:

```bash
bash run.sh
```

### After building AppImage

```bash
./OSRSProfitAdvisor-x86_64.AppImage
```

### After installing .deb package

```bash
sudo apt install ./osrs-profit-advisor_0.1.0_amd64.deb
osrs-profit-advisor
```

Or find "OSRS Profit Advisor" in your application menu.

### After system-wide installation

```bash
osrs-profit-advisor
```

Or find "OSRS Profit Advisor" in your application menu.

## Troubleshooting

### "Python 3 is not installed"

Install Python using your package manager (see "Install system dependencies" above).

### "Permission denied" when running setup scripts

Make the scripts executable:

```bash
chmod +x *.sh
```

Or use:

```bash
bash setup.sh
```

### Virtual environment activation fails

Make sure you're using `source` and not `.`:

```bash
source .venv/bin/activate  # Correct
. .venv/bin/activate       # Also works
.venv/bin/activate         # Does not work
```

### PySide6 installation fails

You may need additional system libraries:

**Ubuntu/Debian:**
```bash
sudo apt install libxkbcommon-x11-0 libdbus-1-3 libfontconfig1 libfreetype6
```

**Fedora/RHEL:**
```bash
sudo dnf install libxkbcommon libdbus fontconfig freetype
```

### Database initialization errors

Make sure the `data/` directory is writable:

```bash
ls -ld data
chmod 755 data
```

### AppImage build fails

If `appimagetool` is not found, install it:

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

## First Use

1. **Launch the app:**
   ```bash
   bash setup.sh && bash run.sh
   ```

2. **Initial sync:**
   - The app automatically syncs price data from the OSRS Wiki API on first run
   - This may take 30-60 seconds depending on internet speed
   - A local SQLite database is created in `data/`

3. **Add recipes:**
   - Open the "Recipes" tab
   - Import recipes from `data/recipes.json` (sample recipes are included)
   - Or add your own recipes using the UI

4. **Explore features:**
   - **Dashboard:** Overview of sync status and top recipes
   - **Item Search:** Browse and search items by name
   - **Recipes:** View and analyze recipe profitability
   - **Price Forecast:** See short-term price trends
   - **Settings:** Configure app behavior

## Updates

To update the app after pulling new changes:

```bash
git pull
bash setup.sh  # Updates dependencies and database schema
```

## Uninstall

### Remove local installation

```bash
rm -rf .venv data logs
```

### Remove AppImage

```bash
rm -f OSRSProfitAdvisor-x86_64.AppImage
```

### Remove .deb package

```bash
sudo apt remove osrs-profit-advisor
```

### Remove system-wide installation

```bash
sudo rm -rf /opt/osrs-profit-advisor
sudo rm /usr/local/bin/osrs-profit-advisor
sudo rm /usr/share/applications/osrs-profit-advisor.desktop
```

## Need help?

- Check the main README.md for project features
- See `docs/` folder for detailed guides
- Run `pytest -v` to verify everything is working
- Check application logs in the `logs/` directory (after first run)
