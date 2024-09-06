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
    
    def __init__(self):
        super().__init__()
        self.check_required_settings()
    
    def check_required_settings(self):
        if not self.FIREBASE_API_KEY:
            raise Exception("FIREBASE_API_KEY is required")
        if not self.FIREBASE_AUTH_DOMAIN:
            raise Exception("FIREBASE_AUTH_DOMAIN is required")
        if not self.FIREBASE_PROJECT_ID:
            raise Exception("FIREBASE_PROJECT_ID is required")
        if not self.FIREBASE_STORAGE_BUCKET:
            raise Exception("FIREBASE_STORAGE_BUCKET is required")
        if not self.FIREBASE_MESSAGING_SENDER_ID:
            raise Exception("FIREBASE_MESSAGING_SENDER_ID is required")
        if not self.FIREBASE_APP_ID:
            raise Exception("FIREBASE_APP_ID is required")
        if not self.FIREBASE_MEASUREMENT_ID:
            raise Exception("FIREBASE_MEASUREMENT_ID is required")
        if not self.FIREBASE_SERVICE_ACCOUNT_KEY_PATH:
            raise Exception("FIREBASE_SERVICE_ACCOUNT_KEY_PATH is required")
        if not self.JWT_SECRET_KEY:
            raise Exception("JWT_SECRET_KEY is required")
        if not self.JWT_ALGORITHM:
            raise Exception("JWT_ALGORITHM is required")

settings = Settings()