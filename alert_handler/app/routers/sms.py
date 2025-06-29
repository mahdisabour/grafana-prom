from fastapi import APIRouter

from app.utils.data_extractor import format_alert_message
from app.adapter.sms import SMSAdapter
from app.core.config import get_setting 


SETTING = get_setting()
PREFIX = "/sms"
router = APIRouter(prefix=PREFIX, tags=["SMS"])


@router.post("/grafana", status_code=200)
async def send_sms(
    data: dict,
) -> None:
    """
    # Description
        send sms
    """
    
    message = format_alert_message(data)
    await SMSAdapter.send(
        phone_numbers=SETTING.sms_config.phone_numbers,
        message_text=message
    )

    