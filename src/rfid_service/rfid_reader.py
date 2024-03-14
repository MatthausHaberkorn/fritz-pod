from ast import Tuple
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from typing import Callable, Optional
import time


class RFIDReader:
    def __init__(self, debounce_time: int = 1) -> None:
        """
        Initializes the RFID reader and the running flag and a debounce time.

        Assumes:
             Nothing.
        Assures:
             An RFIDReader instance is created with a SimpleMFRC522 reader and a
             running flag set to True.
        """
        self.reader: SimpleMFRC522 = SimpleMFRC522()
        self.last_read_id = None
        self.last_read_time = 0
        self.debounce_time = debounce_time

    def read(self) -> tuple[Optional[int], Optional[str]]:
        """
        Reads an RFID tag and returns its ID and text.

        Assumes:
            The RFID reader is properly connected and functioning.
        Assures:
            Returns the ID and text of the read tag if the read is successful and not ignored due to the debounce time.
            Returns None, None if the read is ignored due to the debounce time.

        Returns:
            A tuple containing the ID and text of the read tag, or None, None if the read is ignored.
        """
        id, text = self.reader.read()

        current_time = time.time()
        if (
            id != self.last_read_id
            or current_time - self.last_read_time >= self.debounce_time
        ):
            self.last_read_id = id
            self.last_read_time = current_time
            return id, text
        return None, None

    def listen_for_card(self, callback: Callable[[int, str], None]) -> None:
        """
        Continuously listens for a card as long as the running flag is True.
        When a card is read, it calls the callback function with the card data and then pauses for a delay.
        The delay prevents the reader from immediately reading the same tag again.

        Assumes:
            The callback is a function that takes an int and a str and returns None.
        Assures:
            The callback function is called with the card data every time a card is read.
            There is a delay of 1 second after each successful read to prevent immediate subsequent reads of the same card.
        """

        try:
            while True:
                id, text = self.read()
                if id is not None and text is not None:
                    callback(id, text)
                time.sleep(1)
        except:
            GPIO.cleanup()
            raise

    def stop_listening(self) -> None:
        """
        Stops the listening loop by setting the running flag to False.

        Assumes:
            Nothing.
        Assures:
            The running flag is set to False, stopping the listening loop.
        """
        self.running = False
