from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "sqlite:///./sockshop_fastapi.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()