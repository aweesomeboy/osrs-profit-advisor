# OSRS Profit Advisor

Local FastAPI web app for tracking Old School RuneScape Grand Exchange prices and profit data.

## Quick Start

Clone and run in one go:

```bash
git clone https://github.com/aweesomeboy/osrs-profit-advisor.git
cd osrs-profit-advisor
chmod +x run.sh
./run.sh
```

Then open your browser:

```
http://127.0.0.1:8000
```

## Manual Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

## Features

- ✓ FastAPI backend with local price cache
- ✓ OSRS Wiki API integration with User-Agent
- ✓ Auto-refresh every 5 minutes (backend) and 60 seconds (frontend)
- ✓ Search, sorting, pagination
- ✓ Real item data from OSRS Wiki
- ✓ Last sync, next sync, API status, stale warnings
- ✓ Manual refresh button
- ✓ Dark OSRS-themed dashboard
- ✓ No login, no database, no external dependencies
- ✓ Works on Linux, macOS, Windows

## API Endpoints

- `GET /` - Dashboard
- `GET /api/health` - API health status
- `GET /api/items` - List items with search, sort, pagination
- `GET /api/items/{item_id}` - Get single item
- `POST /api/refresh` - Manually refresh prices

## Query Parameters for /api/items

- `search` - Search by item name or ID
- `sort` - Sort field (name, item_id, high_price, low_price, margin, roi)
- `order` - asc or desc
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

## Requirements

- Python 3.8+
- No external GUI framework needed

## Configuration

Edit `osrs_api.py` to customize:
- `SYNC_INTERVAL` - How often to refresh prices (default: 300 seconds / 5 minutes)
- `TIMEOUT` - API request timeout (default: 30 seconds)
- `USER_AGENT` - Your contact email in User-Agent header

## Project Structure

```
osrs-profit-advisor/
├── app.py              # FastAPI application
├── osrs_api.py         # OSRS Wiki API integration
├── requirements.txt    # Python dependencies
├── run.sh              # Startup script
├── README.md           # This file
├── templates/
│   └── index.html      # Frontend HTML
├── static/
│   ├── style.css       # Dashboard styling
│   └── app.js          # Frontend logic
└── tests/
    └── test_api.py     # API tests
```

## Troubleshooting

### Port 8000 already in use
```bash
python3 -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

### API won't connect
- Check your internet connection
- Verify OSRS Wiki API is reachable: https://prices.runescape.wiki/api/v1/osrs/latest
- Check browser console (F12) for errors

### No items showing
- Wait 5-10 seconds for initial sync
- Click "Refresh Now" button
- Check "API status" indicator

### Virtual environment issues
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Notes

This application intentionally avoids:
- React, Vue, or other heavy frameworks
- Vite, Webpack, or build systems
- Node.js or npm
- SQLite or any database
- Login systems or authentication
- Desktop application wrappers

It's a simple, lightweight local web app designed to run on Linux with one command.

## License

MIT License
