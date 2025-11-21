from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str | None = None
    fibo_url: str = 'https://api.fibo.example'

settings = Settings()
