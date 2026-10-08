# .deb package guide

## Requirements

- Debian/Ubuntu-based Linux
- `dpkg-deb` or `dpkg-buildpackage`
- Python packaging tools

## Example approach

```bash
mkdir -p build/deb/usr/bin/osrs-profit-advisor
cp -r osrs_profit_advisor build/deb/usr/lib/osrs-profit-advisor/
cp run.py build/deb/usr/bin/osrs-profit-advisor/run.py
```

Create a `DEBIAN/control` file with package metadata and then build:

```bash
dpkg-deb --build build/deb osrs-profit-advisor.deb
```

## Notes

- Add a desktop file under `/usr/share/applications/`.
- Install the package with `sudo dpkg -i osrs-profit-advisor.deb`.
- If there are missing dependencies, install them separately with `apt`.
