from typing import Callable
from rfid_reader import RFIDReader
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RFIDData:
    id: int
    text: str
    timestamp: datetime = field(default_factory=datetime.now)


class RFIDService:
    def __init__(
        self,
        log_callback: Callable[[int, str], None],
        store_callback: Callable[[int, str], None],
        send_callback: Callable[[int, str], None],
    ) -> None:
        """
        Initializes the RFIDService with three callback functions and an RFIDReader.
        The callback functions should take RFIDData as an argument.

        Assures:
            An RFIDService instance is created with three callback functions and an RFIDReader.
        """
        self.log_callback = log_callback
        self.store_callback = store_callback
        self.send_callback = send_callback
        self.reader = RFIDReader()

    def handle_data(self, id: int, text: str) -> None:
        """
        Handles the data from the RFID reader.

        Assures:
            The log_callback, store_callback, and send_callback functions are called with the card data.
        """
        data = RFIDData(id, text)
        print(f"Recieved new RFID data with {str(data)}")
        self.log_callback(data)
        self.store_callback(data)
        self.send_callback(data)

    def start(self) -> None:
        """
        Starts the RFID reader listening for cards.

        Assumes:
            The RFID reader is not currently listening for cards.
        Assures:
            The RFID reader starts listening for cards, and the handle_data method is called with the card data every time a card is read.
        """
        self.reader.listen_for_card(self.handle_data)
        print("Service started")

    def stop(self) -> None:
        """
        Stops the RFID reader from listening for cards.

        Assumes:
            The RFID reader is currently listening for cards.
        Assures:
            The RFID reader stops listening for cards.
        """
        self.reader.stop_listening()
