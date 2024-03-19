from pydantic import BaseModel


class PlayResponse(BaseModel):
    card_id: int
    file_name: str

    class Config:
        from_attributes = True
