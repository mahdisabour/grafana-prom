import httpx

from app.core.config import get_setting
from app.utils.exceptions import ServiceUnavailableException


SETTING = get_setting()


class SMSAdapter:

    @staticmethod
    async def send(phone_numbers: list[str], message_text: str) -> None:
        if SETTING.sms_config.mock:
            return None

        async with httpx.AsyncClient() as client:
            for phone_number in phone_numbers:
                payload = {
                    'userName': SETTING.sms_config.username,
                    'password': SETTING.sms_config.password,
                    'senderNumber': SETTING.sms_config.sender_number,
                    'reciverNumber': phone_number,
                    'smsText': message_text
                }

                try:
                    response = await client.post(SETTING.sms_config.url, data=payload)
                    response.raise_for_status()
                except httpx.HTTPError:
                    # Optionally log the failure per number
                    raise ServiceUnavailableException("SMS service is unavailable")


if __name__ == "__main__":
    ...
