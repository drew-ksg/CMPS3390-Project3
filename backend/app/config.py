# TODO: Load settings from .env using Pydantic BaseSettings (SECRET_KEY, DATABASE_URL)
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    Database_URL: str
    API_KEY: str
    SECRET_KEY: str
    Algorithm: str = "H256"
    Access_Token_Expire_Minutes: int = 30
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()


