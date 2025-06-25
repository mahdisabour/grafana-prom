from fastapi import APIRouter

PREFIX = "/sms"


router = APIRouter(prefix=PREFIX, tags=["SMS"])


@router.post("/", status_code=200)
async def send_sms(
    data: dict,
):
    """
    # Description
        send sms

    """
    print(data)
    return None