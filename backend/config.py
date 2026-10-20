import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Automatically load from root .env file if present
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

class Settings(BaseModel):
    app_name: str = "Veritas AI - Legal Document Intelligence & Investigation Platform"
    app_version: str = "1.0.0"
    event_tagline: str = "Kritical Hacks 2026: Don't Just Read the Contract. Investigate It."
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    tinyfish_api_key: str = os.getenv("TINYFISH_API_KEY", "")
    max_upload_size_mb: int = 25
    allowed_extensions: list[str] = [".pdf", ".png", ".jpg", ".jpeg"]

settings = Settings()
