from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Boolean, Column, Integer, String, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import uvicorn
import os

# Create a new SQLAlchemy engine and sessionmaker
engine = create_engine("duckdb:///fritzpod.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new SQLAlchemy base class
Base = declarative_base()

card_id_seq = Sequence("card_id_seq")


# Define a new RFIDCard model
class RFIDCard(Base):
    __tablename__ = "rfidcards"

    id = Column(
        Integer,
        card_id_seq,
        primary_key=True,
        index=True,
        server_default=card_id_seq.next_value(),
    )
    rfid = Column(String, unique=True, index=True)
    audio_file = Column(String)
    



# Create the RFIDCard table
Base.metadata.create_all(bind=engine)

app = FastAPI()


current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "app/static")
# Mount the static files router
app.mount("/admin", StaticFiles(directory=static_dir), name="static")


@app.post("/rfid/{rfid}")
async def create_rfid(rfid: str, audio_file: str):
    # Create a new SQLAlchemy session
    session = SessionLocal()

    # Create a new RFIDCard
    rfid_card = RFIDCard(rfid=rfid, audio_file=audio_file)

    # Add the new RFIDCard to the session and commit it
    session.add(rfid_card)
    session.commit()

    return {"message": f"Created RFID {rfid} with audio file {audio_file}"}


@app.get("/rfid/{rfid}")
async def get_rfid(rfid: str):
    # Create a new SQLAlchemy session
    session = SessionLocal()

    # Get the RFIDCard with the specified RFID
    rfid_card = session.query(RFIDCard).filter(RFIDCard.rfid == rfid).first()

    # Return the RFIDCard's audio file
    return {"audio_file": rfid_card.audio_file}

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
