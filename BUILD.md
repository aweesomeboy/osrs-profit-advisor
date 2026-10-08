# Build system and packaging

## Files included

- `setup.sh` - Basic setup for running locally
- `run.sh` - Quick launcher after setup
- `build_appimage.sh` - Build standalone AppImage
- `build_deb.sh` - Build .deb package for Debian/Ubuntu
- `install.sh` - Install system-wide
- `dev-setup.sh` - Setup for development
- `setup-menu.sh` - Interactive menu (all options)
- `quick-setup.sh` - Fast one-command setup
- `osrs-profit-advisor.desktop` - Desktop menu entry

## Quick reference

```bash
# First time setup
bash quick-setup.sh

# Run the app
bash run.sh

# Interactive menu (more options)
bash setup-menu.sh

# Build AppImage (portable)
bash build_appimage.sh

# Build .deb package
bash build_deb.sh

# Install system-wide
sudo bash install.sh

# Development setup
bash dev-setup.sh
```

## Detailed guides

See `docs/SETUP.md` for complete documentation.
