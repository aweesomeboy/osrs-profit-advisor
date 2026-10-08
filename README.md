# OSRS Profit Advisor

Local FastAPI web app for tracking Old School RuneScape Grand Exchange prices and profit data.

## Quick start

```bash
chmod +x run.sh
./run.sh
```

Or run manually:

```bash
python3 -m uvicorn app:app --reload
```

Open: http://127.0.0.1:8000

## Features

- FastAPI backend with local price cache
- OSRS Wiki API integration with User-Agent
- Auto-refresh every 60 seconds on the frontend and every 5 minutes in backend
- Search, sorting, pagination, and table display
- Last sync, next sync, API status, stale warning, and item count
- Manual refresh button
- Works without login or database setup

## API

- GET /
- GET /api/health
- GET /api/items
- GET /api/items/{item_id}
- POST /api/refresh

## Notes

This app intentionally avoids React, Vite, Node.js, and any heavy build system. It is a lightweight Python app designed for a simple Linux local web setup.
