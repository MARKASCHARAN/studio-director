import os
from dotenv import load_dotenv

# Load correct environment file
ENV = os.getenv("ENV", "local")

if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.local")

class Settings:
    BRIA_API_KEY: str = os.getenv("BRIA_API_KEY")
    ENV: str = ENV

settings = Settings()
