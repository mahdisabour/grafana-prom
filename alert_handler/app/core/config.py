from functools import lru_cache

from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict


class SMSConfig(BaseSettings):
    username: str = "username"
    password: str = "password"
    sender_number: str = "sernder_number"
    default_admin_number: str = "09145178976"   
    url: str = "http://url.com" 
    mock: bool = False


class Setting(BaseSettings):
    app_version: str = "1.0.0"
    prefix: str = "/api"
    
    sms_config: SMSConfig

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8',
        env_nested_delimiter='__', env_nested_max_split=1
    )


@lru_cache
def get_setting():
    return Setting()


if __name__ == "__main__":
    print(Setting().model_dump())