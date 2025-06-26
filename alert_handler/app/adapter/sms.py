import httpx

from app.core.config import get_setting
from app.utils.exceptions import ServiceUnavailableException


SETTING = get_setting()


class SMSAdapter:

    @staticmethod
    async def send(phone_number: str, message_text: str) -> None:
        if SETTING.sms_config.mock:
            return None
        
        payload = {
            'userName': SETTING.sms_config.username,
            'password': SETTING.sms_config.password,
            'senderNumber': SETTING.sms_config.sender_number,
            'recieverNumber': phone_number,
            'smsText': message_text
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(SETTING.sms_config.url, data=payload)
                response.raise_for_status()
            except httpx.HTTPError as e:
                ServiceUnavailableException(f"SMS service is unavailable")
        

if __name__ == "__main__":
    ...