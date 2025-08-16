from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Supabase Configuration
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # Gemini AI Configuration
    gemini_api_key: str
    
    # JWT Configuration
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    
    # Debug mode
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False
        
settings = Settings()