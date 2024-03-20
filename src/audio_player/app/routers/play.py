from fastapi import APIRouter, HTTPException, status

from app.backend.settings import settings
from app.schemas.play import PlayResponse
from app.services.player import get_file_path, play_file
from app.services.pod_management import get_rfid_card, send_play_statistic

router = APIRouter()

rfid_card_service_url = f"{settings.pod_management_service_url}/rfid_card"


@router.post("/{rfid_code}/{writable_tag}", response_model=PlayResponse)
async def play(rfid_code: str, writable_tag: str) -> PlayResponse:
    # get title from management service

    rfid_card = await get_rfid_card(rfid_code, writable_tag)
    # search for file on local storage
    # if file not found, raise 404
    # play file
    # send play statistic to management service

    file_name = rfid_card["file_name"]
    file_path = get_file_path(file_name)
    if file_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {file_name} not found",
        )

    play_file(file_path)
    play_statistic = await send_play_statistic(rfid_code, writable_tag)

    response = {
        "card_id": rfid_card["card_id"],
        "file_name": file_name,
    }

    return PlayResponse.model_validate(response)
