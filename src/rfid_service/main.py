from rfid_service import RFIDService, RFIDData
from api_client import APIClient


callbacks = []


def register_callback(callback):
    callbacks.append(callback)
    return callback


@register_callback
def log_data(data: RFIDData) -> None:
    print(f"Log data for: {str(data)}")


@register_callback
def store_data(data: RFIDData) -> None:
    print(f"Store data for: {str(data)}")


api_client = APIClient()


@register_callback
def request_audio(data: RFIDData) -> None:
    return api_client.request_audio(data)


def main():
    service = RFIDService(callbacks)
    service.start()


if __name__ == "__main__":
    main()
