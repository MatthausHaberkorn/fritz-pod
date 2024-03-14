from typing import Callable, List
from rfid_reader import RFIDReader
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RFIDData:
    id: int
    text: str
    timestamp: datetime = field(default_factory=datetime.now)


class RFIDService:
    def __init__(self, callbacks: List[Callable[[RFIDData], None]]) -> None:
        """
        Initializes the RFIDService with a list of callback functions and an RFIDReader.
        Each callback function should take an RFIDData instance as an argument.

        Assures:
            An RFIDService instance is created with a list of callback functions and an RFIDReader.
        """
        self.callbacks = callbacks
        self.reader = RFIDReader()

    def handle_data(self, id: int, text: str) -> None:
        """
        Handles the data from the RFID reader.

        Assures:
            Each callback function in self.callbacks is called with the card data.
        """
        data = RFIDData(id, text)
        print(f"Recieved new RFID data with {str(data)}")
        for callback in self.callbacks:
            callback(data)

    def start(self) -> None:
        """
        Starts the RFID reader listening for cards.

        Assumes:
            The RFID reader is not currently listening for cards.
        Assures:
            The RFID reader starts listening for cards, and the handle_data method is called with the card data every time a card is read.
        """
        print("Service started")
        self.reader.listen_for_card(self.handle_data)

    def stop(self) -> None:
        """
        Stops the RFID reader from listening for cards.

        Assumes:
            The RFID reader is currently listening for cards.
        Assures:
            The RFID reader stops listening for cards.
        """
        self.reader.stop_listening()
