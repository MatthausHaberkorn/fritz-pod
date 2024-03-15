# app/api/endpoints/rfid_cards.py
from fastapi import APIRouter, HTTPException, Depends
from app.api.models.rfid_card import RFIDCardCreate
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.crud import rfid_card as rfid_card_crud

router = APIRouter()


@router.post("/{rfid_code}/{writable_tag}")
async def create_rfid_card(
    rfid_code: str,
    writable_tag: str,
    card: RFIDCardCreate,
    db: Session = Depends(get_db),
):
    db_card = rfid_card_crud.get_by_rfid_code_and_writable_tag(
        db, rfid_code=rfid_code, writable_tag=writable_tag
    )
    if db_card:
        raise HTTPException(
            status_code=400,
            detail=f"RFID_code {rfid_code} and writable_tag {writable_tag} are already in use",
        )
    return rfid_card_crud.create(db=db,rfid_code=rfid_code, writable_tag=writable_tag, card=card)
