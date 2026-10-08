from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import asyncio

from osrs_api import OSRSAPIManager

osrs_api = OSRSAPIManager()
sync_task = None


async def sync_prices():
    while True:
        try:
            await osrs_api.refresh_data()
        except Exception as exc:
            osrs_api.error = str(exc)
        await asyncio.sleep(osrs_api.sync_interval)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sync_task
    await osrs_api.refresh_data()
    sync_task = asyncio.create_task(sync_prices())
    try:
        yield
    finally:
        if sync_task:
            sync_task.cancel()
            try:
                await sync_task
            except asyncio.CancelledError:
                pass


app = FastAPI(title="OSRS Profit Advisor", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return FileResponse("templates/index.html")


@app.get("/api/health")
async def health():
    return osrs_api.get_health()


@app.get("/api/items")
async def get_items(
    search: str | None = Query(default=None),
    sort: str = Query(default="name"),
    order: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return osrs_api.get_items(
        search=search,
        sort_by=sort,
        sort_order=order,
        page=page,
        page_size=page_size,
    )


@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    item = osrs_api.get_item(item_id)
    if item is None:
        return {"error": f"Item {item_id} not found"}
    return item


@app.post("/api/refresh")
async def refresh():
    await osrs_api.refresh_data()
    return osrs_api.get_health()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
