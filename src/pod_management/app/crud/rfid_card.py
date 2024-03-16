from sqlalchemy import select
from app.db.models.rfid_card import RFIDCard
from app.api.models.rfid_card import RFIDCardCreate
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


async def create(db: AsyncSession, rfid_code: str, writable_tag: str, card: RFIDCardCreate):
    db_card = RFIDCard(
        rfid_code=rfid_code, writable_tag=writable_tag, **card.model_dump()
    )
    db.add(db_card)
    await db.commit()
    await db.refresh(db_card)
    return db_card

async def get_by_rfid_code_and_writable_tag(db: AsyncSession, rfid_code: str, writable_tag: bool):
    result = await db.execute(
        select(RFIDCard).where(RFIDCard.rfid_code == rfid_code, RFIDCard.writable_tag == writable_tag)
    )
    return result.scalars().first()
