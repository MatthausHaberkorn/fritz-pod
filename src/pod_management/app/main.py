from fastapi import FastAPI
from app.api import rfid_card

app = FastAPI()

app.include_router(rfid_card.router, prefix="/rfid_card", tags=["rfid_card"])