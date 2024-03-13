from rfid_service import RFIDService, RFIDData
from api_client import APIClient


def main():
    def log_data(data: RFIDData) -> None:
        print(f"Log data for: {str(data)}")

    def store_data(data: RFIDData) -> None:
        print(f"Store data for: {str(data)}")

    api_client = APIClient()
    service = RFIDService(log_data, store_data, api_client.request_audio)
    service.start()


if __name__ == "__main__":
    main()
