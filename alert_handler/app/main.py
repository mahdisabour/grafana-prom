"""
    Backend Main module
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_setting
from app.routers.sms import router as sms_router

def get_application() -> FastAPI:
    application = FastAPI(
        version=get_setting().app_version, title="alert_handler",
    )
    application.include_router(sms_router, prefix=get_setting().prefix)
    return application


app: FastAPI = get_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
