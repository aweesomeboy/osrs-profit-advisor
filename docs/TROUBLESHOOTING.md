# OSRS Profit Advisor - Setup Troubleshooting

## Common Issues and Solutions

### Issue 1: "PEP 668" error or "externally-managed-environment"

**What it means:** Modern Debian/Ubuntu systems block pip from installing packages globally to prevent conflicts.

**Solution:** Make sure you're using a virtual environment:

```bash
bash quick-setup.sh
```

Or manually:

```bash
sudo apt install python3-full python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue 2: "No such file or directory: .venv/bin/activate"

**What it means:** The virtual environment wasn't created properly.

**Solution:** Remove and recreate it:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or use the fix script:

```bash
bash fix-setup.sh
```

### Issue 3: "ModuleNotFoundError: No module named 'PySide6'"

**What it means:** PySide6 didn't install or the virtual environment isn't activated.

**Solution:**

1. Make sure you activated the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Reinstall PySide6:
   ```bash
   pip install --upgrade PySide6
   ```

3. Test it works:
   ```bash
   python3 -c "from PySide6.QtWidgets import QApplication; print('OK')"
   ```

### Issue 4: PySide6 installation fails

**What it means:** Missing system libraries.

**Solution on Ubuntu/Debian/Linux Lite:**

```bash
sudo apt install libxkbcommon-x11-0 libdbus-1-3 libfontconfig1 libfreetype6
pip install --upgrade PySide6
```

**Solution on Fedora/RHEL:**

```bash
sudo dnf install libxkbcommon libdbus fontconfig freetype
pip install --upgrade PySide6
```

### Issue 5: "command not found: python3"

**Solution:**

**Ubuntu/Debian/Linux Lite:**
```bash
sudo apt update
sudo apt install python3 python3-full python3-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

### Issue 6: Setup script permission denied

**Solution:**

```bash
chmod +x *.sh
bash quick-setup.sh
```

Or use `bash` directly (no execute needed):

```bash
bash quick-setup.sh
```

### Issue 7: Database initialization fails

**Solution:**

1. Make sure the data folder exists:
   ```bash
   mkdir -p data
   chmod 755 data
   ```

2. Try again:
   ```bash
   bash quick-setup.sh
   ```

### Issue 8: "error: externally-managed-environment" even in venv

**What it means:** The venv wasn't created with `--upgrade-deps` or python3-full isn't installed.

**Solution:**

```bash
# On Debian/Ubuntu 12.2+
sudo apt install python3-full

# Remove and recreate venv
rm -rf .venv
python3 -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install -r requirements.txt
```

## Step-by-step fix

If you're still having trouble, run this:

```bash
#!/bin/bash
# 1. Install system requirements
sudo apt update
sudo apt install -y python3 python3-full python3-venv python3-pip \
  libxkbcommon-x11-0 libdbus-1-3 libfontconfig1 libfreetype6

# 2. Remove old files
rm -rf .venv build dist *.spec OSRSProfitAdvisor.AppDir

# 3. Create fresh venv
python3 -m venv .venv --upgrade-deps

# 4. Activate and install
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Test
python3 run.py
```

## Verify everything works

```bash
source .venv/bin/activate

# Check Python
python3 --version

# Check PySide6
python3 -c "from PySide6.QtWidgets import QApplication; print('✓ PySide6')"

# Check requests
python3 -c "import requests; print('✓ requests')"

# Check yaml
python3 -c "import yaml; print('✓ yaml')"

# Run the app
python run.py
```

## Still stuck?

If you're on Linux Lite and still having issues:

1. Open a terminal
2. Copy-paste this entire block:

```bash
cd ~/osrs-profit-advisor
sudo apt install -y python3-full python3-venv python3-pip
rm -rf .venv
python3 -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install PySide6 requests PyYAML pytest
python run.py
```

3. The app should now start

## After setup

Once it works, you can:

- Run the app: `bash run.sh`
- Build AppImage: `bash build_appimage.sh`
- Run tests: `pytest -v`
- Update: `git pull && bash quick-setup.sh`
