from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.rfid_card import get_by_rfid_code_and_writable_tag
from app.crud.play_statistic import create
from app.api.models.play_statistic import PlayStatisticResponse
from fastapi import status

router = APIRouter()


@router.post("/{rfid_code}/{writable_tag}", response_model=PlayStatisticResponse)
async def create_play_statistic(
    rfid_code: str, writable_tag: str, db: AsyncSession = Depends(get_db)
):
    """
    Create a new PlayStatistic record.

    Args:
        rfid_code (str): The RFID code of the card.
        writable_tag (str): The writable tag of the card.
        db (AsyncSession): The database session.

    Returns:
        PlayStatistic: The new PlayStatistic record, or HTTPException if no matching RFIDCard record is found.
    """
    rfid_card = await get_by_rfid_code_and_writable_tag(db, rfid_code, writable_tag)
    if rfid_card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="RFIDCard not found"
        )

    return await create(db, rfid_code, writable_tag)
