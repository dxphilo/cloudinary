from pydantic import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv(".env")

class Settings(BaseSettings):
    APP_NAME: str
    PORT: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_API_KEY: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()