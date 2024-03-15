from app.db.models.rfid_card import RFIDCard
from app.api.models.rfid_card import RFIDCardCreate
from sqlalchemy.orm import Session


def create(db: Session, rfid_code: str, writable_tag: str, card: RFIDCardCreate):
    db_card = RFIDCard(
        rfid_code=rfid_code, writable_tag=writable_tag, **card.model_dump()
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def get_by_rfid_code_and_writable_tag(db: Session, rfid_code: str, writable_tag: bool):
    return (
        db.query(RFIDCard)
        .filter(RFIDCard.rfid_code == rfid_code, RFIDCard.writable_tag == writable_tag)
        .first()
    )
