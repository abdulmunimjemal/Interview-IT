from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "User Management Microservice"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "This is a user management microservice using Firebase Auth for user authentication."
    FIREBASE_API_KEY: str
    FIREBASE_AUTH_DOMAIN: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_MESSAGING_SENDER_ID: str
    FIREBASE_APP_ID: str
    FIREBASE_MEASUREMENT_ID: str
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str
    FIREBASE_DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = "placeholder"
    JWT_ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()