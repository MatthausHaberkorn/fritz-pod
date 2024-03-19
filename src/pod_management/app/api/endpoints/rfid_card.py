# app/api/endpoints/rfid_cards.py
from app.api.models.rfid_card import RFIDCardCreate, RFIDCardResponse
from app.crud import rfid_card as rfid_card_crud
from app.db.session import get_db
from app.dependencies import pagination
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/{rfid_code}/{writable_tag}", response_model=RFIDCardResponse)
async def create_rfid_card(
    rfid_code: str,
    writable_tag: str,
    card: RFIDCardCreate,
    db: AsyncSession = Depends(get_db),
) -> RFIDCardResponse:
    db_card = await rfid_card_crud.get_by_rfid_code_and_writable_tag(
        db, rfid_code=rfid_code, writable_tag=writable_tag
    )
    if db_card:
        raise HTTPException(
            status_code=400,
            detail=f"RFID_code {rfid_code} and writable_tag {writable_tag} are already in use",
        )
    return await rfid_card_crud.create(
        db=db, rfid_code=rfid_code, writable_tag=writable_tag, card=card
    )


@router.get("/{rfid_code}/{writable_tag}")
async def get_rfid_card(
    rfid_code: str,
    writable_tag: str,
    db: AsyncSession = Depends(get_db),
):
    return await rfid_card_crud.get_by_rfid_code_and_writable_tag_or_404(
        db, rfid_code=rfid_code, writable_tag=writable_tag
    )


@router.get("/")
async def read_rfid_cards(
    db: AsyncSession = Depends(get_db), pagination_params: tuple = Depends(pagination)
):
    skip, limit = pagination_params
    cards = await rfid_card_crud.get_rfid_cards(db, skip=skip, limit=limit)
    return cards
