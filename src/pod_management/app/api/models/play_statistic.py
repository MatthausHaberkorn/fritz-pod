import datetime
from pydantic import BaseModel


class PlayStatisticResponse(BaseModel):
    id: int
    card_id: int
    created_at: datetime
