from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.constants import FileType


class RFIDCardCreate(BaseModel):
    file_name: str
    file_type: FileType
    date: Optional[datetime]
    duration: Optional[float] = Field(..., gt=0)
    size: Optional[float] = Field(..., gt=0)
    source: Optional[str]
    display_text: Optional[str]
