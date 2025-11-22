import os
from dotenv import load_dotenv

# Load correct .env file depending on environment
ENV = os.getenv("ENV", "local")

if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.local")

class Settings:
    ENV: str = ENV
    BRIA_API_KEY: str = os.getenv("BRIA_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()

# Validate keys on startup
if not settings.BRIA_API_KEY:
    print("⚠️ WARNING: BRIA_API_KEY missing!")

if not settings.GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY missing!")
