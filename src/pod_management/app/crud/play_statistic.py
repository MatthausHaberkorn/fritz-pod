from typing import Optional

from app.api.models.play_statistic import PlayStatisticResponse
from app.db.models.play_statistic import PlayStatistic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create(db: AsyncSession, card_id: int) -> Optional[PlayStatistic]:
    """
    Create a new PlayStatistic record.

    Assumes:
        - `rfid_code` and `writable_tag` correspond to an existing RFIDCard record in the database.

    Assures:
        - A new PlayStatistic record is created and associated with the RFIDCard record that matches the provided `rfid_code` and `writable_tag`.
        - The new PlayStatistic record is returned, or None if no matching RFIDCard record is found.

    Returns:
        PlayStatistic: The new PlayStatistic record, or None if no matching RFIDCard record is found.
    """

    play_statistic = PlayStatistic(card_id=card_id)
    db.add(play_statistic)
    await db.commit()
    await db.refresh(play_statistic)
    return PlayStatisticResponse.model_validate(play_statistic)


async def get_play_statistics(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(PlayStatistic).offset(skip).limit(limit))
    return result.scalars().all()
