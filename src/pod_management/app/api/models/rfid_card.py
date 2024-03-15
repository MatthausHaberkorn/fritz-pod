from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.constants import FileType


class RFIDCardCreate(BaseModel):
    file_name: str
    file_type: FileType
    date: Optional[datetime]
    duration: Optional[float]
    size: Optional[float]
