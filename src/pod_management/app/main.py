import contextlib
from fastapi import FastAPI

from .db.session import create_all_tables
from .api.endpoints import rfid_card


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(rfid_card.router, prefix="/rfid_card", tags=["rfid_card"])
