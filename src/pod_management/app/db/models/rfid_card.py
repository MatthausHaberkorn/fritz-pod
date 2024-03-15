from sqlalchemy import Column, Integer, Sequence, String, DateTime, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from app.constants import FileType


Base = declarative_base()


card_id_seq = Sequence("card_id_seq")


class RFIDCard(Base):
    """
    Represents an RFID card in the database.

    Attributes:
    card_id: A unique integer that serves as the primary key.
    rfid_code: A unique string that represents the RFID of the card, fixed by the manufacturer.
    writable_tag: A writable string that represents a tag on the RFID card.
    file_name: A string that represents the name of a file associated with the RFID card. This is the name the file will be stored under in object storage and the name it will have when downloaded to the local file system for usage.
    file_type: An enumerated type that can take the values 'audio', 'video', or 'image'.
    date: A datetime that represents when the file was created or last modified.
    duration: A float that represents the duration of the file in some unit of time.
    size: A float that represents the size of the file in some unit of measurement.
    """

    __tablename__ = "rfid_cards"

    card_id = Column(
        Integer,
        card_id_seq,
        primary_key=True,
        index=True,
        server_default=card_id_seq.next_value(),
        comment="A unique integer that serves as the primary key.",
    )
    rfid_code = Column(
        String,
        unique=True,
        index=True,
        comment="A unique string that represents the RFID of the card, fixed by the manufacturer.",
    )
    writable_tag = Column(
        String,
        unique=True,
        index=True,
        comment="A writable string that represents a tag on the RFID card.",
    )
    file_name = Column(
        String,
        comment="A string that represents the name of a file associated with the RFID card. This is the name the file will be stored under in object storage and the name it will have when downloaded to the local file system for usage.",
    )
    file_type = Column(
        Enum(FileType),
        comment="An enumerated type that can take the values 'audio', 'video', or 'image'.",
    )
    date = Column(
        DateTime,
        comment="A datetime that represents when the file was created or last modified.",
    )
    duration = Column(
        Float,
        comment="A float that represents the duration of the file in some unit of time.",
    )
    size = Column(
        Float,
        comment="A float that represents the size of the file in some unit of measurement.",
    )
