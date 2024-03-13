from rfid_service import RFIDData


class APIClient:
    def request_audio(self, data: RFIDData) -> None:
        # Code to send the data over a network
        print(f"Call endpoint for playing sound with {str(data)}")
