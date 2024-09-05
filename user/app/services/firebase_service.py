import pyrebase
from app.core.config import settings

class FirebaseService:
    def __init__(self):
        config = {
            "apiKey": settings.FIREBASE_API_KEY,
            "authDomain": settings.FIREBASE_AUTH_DOMAIN,
            "projectId": settings.FIREBASE_PROJECT_ID,
            "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
            "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
            "appId": settings.FIREBASE_APP_ID,
            "measurementId": settings.FIREBASE_MEASUREMENT_ID,
            "databaseURL": settings.FIREBASE_DATABASE_URL
        }
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
    
    def register_user(self, email, password):
        self.auth.create_user_with_email_and_password(email, password)
    
    def login_user(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)

    def refresh_token(self, refresh_token):
        return self.auth.refresh(refresh_token)