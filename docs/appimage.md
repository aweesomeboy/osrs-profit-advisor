# AppImage build guide

## Requirements

- Linux desktop environment
- `appimagetool` or a recent AppImage builder
- Python dependencies installed

## Example flow

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m PyInstaller --onefile --noconsole --name OSRSProfitAdvisor run.py
```

Then package the generated binary with `appimagetool` or a custom `.desktop` launcher. Place the generated AppImage in a release folder.

## Notes

- Use a desktop entry file with the proper icon and categories.
- Keep the runtime dependencies bundled or rely on system libraries.
- Test the AppImage on a clean Linux environment before release.
