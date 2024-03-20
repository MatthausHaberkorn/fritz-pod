import contextlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from settings import settings

from .api.endpoints import download, play_statistic, rfid_card
from .db.session import create_all_tables


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    if settings.debug:
        print(f"Loaded project with the following settings:\n{settings}")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(rfid_card.router, prefix="/rfid_card", tags=["rfid_card"])
app.include_router(play_statistic.router, prefix="/play_stats", tags=["play_stats"])
app.include_router(download.router, prefix="/db", tags=["db"])

app.mount("/db", StaticFiles(directory="app/local_db"), name="db")
