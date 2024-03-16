from fastapi import HTTPException
from sqlalchemy import select
from app.db.models.rfid_card import RFIDCard
from app.api.models.rfid_card import RFIDCardCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status


async def create(
    db: AsyncSession, rfid_code: str, writable_tag: str, card: RFIDCardCreate
):
    db_card = RFIDCard(
        rfid_code=rfid_code, writable_tag=writable_tag, **card.model_dump()
    )
    db.add(db_card)
    await db.commit()
    await db.refresh(db_card)
    return db_card


async def get_by_rfid_code_and_writable_tag(
    db: AsyncSession, rfid_code: str, writable_tag: str
):
    result = await db.execute(
        select(RFIDCard).where(
            RFIDCard.rfid_code == rfid_code, RFIDCard.writable_tag == writable_tag
        )
    )
    return result.scalars().first()


async def get_by_rfid_code_and_writable_tag_or_404(
    db: AsyncSession, rfid_code: str, writable_tag: str
):
    result = await db.execute(
        select(RFIDCard).where(
            RFIDCard.rfid_code == rfid_code, RFIDCard.writable_tag == writable_tag
        )
    )
    card = result.scalars().first()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFID_code {rfid_code} and writable_tag {writable_tag} not found",
        )
    return card


async def get_rfid_cards(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(RFIDCard).offset(skip).limit(limit))
    return result.scalars().all()
