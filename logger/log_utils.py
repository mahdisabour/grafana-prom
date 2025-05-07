import os
import logging
from logging.config import dictConfig

def get_log_config(log_level: str) -> dict:
    log_level = log_level.upper()
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "access": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn.error": {
                "level": log_level,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": log_level,
                "handlers": ["access"],
                "propagate": False,
            },
        },
        "root": {
            "level": log_level,
            "handlers": ["default"],
        }
    }


class LogClass:
    @staticmethod
    def get_logger(name: str = "root"):
        CONFIG = get_log_config(os.getenv("LOG_LEVEL", "INFO"))
        dictConfig(CONFIG)
        return logging.getLogger(name)