from datetime import datetime
from typing import Optional

from app.constants import FileType
from pydantic import BaseModel, Field


class RFIDCardCreate(BaseModel):
    file_name: str
    file_type: FileType
    date: Optional[datetime]
    duration: Optional[float] = Field(..., gt=0)
    size: Optional[float] = Field(..., gt=0)
    source: Optional[str]
    display_text: Optional[str]

    class Config:
        from_attributes = True


class RFIDCardResponse(RFIDCardCreate):
    card_id: int
    rfid_code: str
    writable_tag: str
    date: datetime

    class Config:
        from_attributes = True
