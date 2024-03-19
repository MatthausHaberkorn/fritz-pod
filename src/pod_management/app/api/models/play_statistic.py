from datetime import datetime

from pydantic import BaseModel


class PlayStatisticResponse(BaseModel):
    play_id: int
    card_id: int
    date: datetime

    class Config:
        from_attributes = True
