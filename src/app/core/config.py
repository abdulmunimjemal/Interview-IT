from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    # JWT
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_expires: int = Field(..., env="JWT_EXPIRES")
    algorithm: str = "HS256"
    # OAuth
    google_client_id: str = Field(..., env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    email_verification_secret: str = Field(..., env="EMAIL_VERIFICATION_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()