import httpx
from app.backend.settings import settings

rfid_card_service_url = f"{settings.pod_management_service_url}/rfid_card"
play_statistic_service_url = f"{settings.pod_management_service_url}/play_stats"


async def get_rfid_card(rfid_code: str, writable_tag: str):
    async with httpx.AsyncClient() as client:
        print(
            f"Getting card informations for rfid_code:{rfid_code} and writable_tag:{writable_tag}"
        )
        response = await client.get(
            f"{rfid_card_service_url}/{rfid_code}/{writable_tag}"
        )
        response.raise_for_status()  # raise exception if the request failed
        rfid_card = response.json()

        return rfid_card


async def send_play_statistic(rfid_code: str, writable_tag: str):
    async with httpx.AsyncClient() as client:
        print(
            f"Getting play statistic info for rfid_code:{rfid_code} and writable_tag:{writable_tag}"
        )
        response = await client.post(
            f"{play_statistic_service_url}/{rfid_code}/{writable_tag}"
        )
        response.raise_for_status()  # raise exception if the request failed
        play_statistic = response.json()

        return play_statistic
