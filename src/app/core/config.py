from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    google_client_id: str = Field(..., env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    email_verification_secret: str = Field(..., env="EMAIL_VERIFICATION_SECRET")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()