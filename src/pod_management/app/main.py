import contextlib
from fastapi import FastAPI

from settings import settings

from .db.session import create_all_tables
from .api.endpoints import rfid_card, play_statistic


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    if settings.debug:
        print(f"Loaded project with the following settings:\n{settings}")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(rfid_card.router, prefix="/rfid_card", tags=["rfid_card"])
app.include_router(play_statistic.router, prefix="/play_stats", tags=["play_stats"])
