from sqlalchemy import Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base


class PlayStatistic(Base):
    """
    The PlayStatistic model represents a record of a play event.

    Attributes:
        play_id: A unique identifier for each play event. This is the primary key.
        date: The date and time when the play event occurred. By default, it's set to the current date and time.
        card_id: A foreign key that references the id of an RFIDCard. This establishes a many-to-one relationship with the RFIDCard model.
        rfid_card: A relationship field that provides access to the associated RFIDCard instance. The 'back_populates' argument indicates that the RFIDCard model has a 'play_statistics' field that points back to this PlayStatistic model.
    """

    __tablename__ = "play_statistics"

    play_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, default=func.now())
    card_id = Column(Integer, ForeignKey("rfid_cards.card_id"))
    rfid_card = relationship("RFIDCard", back_populates="play_statistics")
