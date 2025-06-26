from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_503_SERVICE_UNAVAILABLE

class UnprocessableEntityException(HTTPException):
    def __init__(self, detail="Unprocessable Entity", headers=None):
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers
        )


class ServiceUnavailableException(HTTPException):
    def __init__(self, detail="Service Unavailable", headers=None):
        super().__init__(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            headers=headers
        )