import pyrebase
from app.core.config import settings
from firebase_admin import auth as admin_auth, initialize_app, credentials


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

        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
        initialize_app(cred)

    def register_user(self, email, password):
        self.auth.create_user_with_email_and_password(email, password)

    def login_user(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        user_info = self.auth.get_account_info(user['idToken'])
        if not user_info['users'][0]['emailVerified']:
            raise ValueError("Email not verified. Please verify your email address.")
        return user

    def refresh_token(self, refresh_token):
        return self.auth.refresh(refresh_token)

    def delete_user(self, uid: str):
        admin_auth.delete_user(uid)

    def change_password(self, id_token: str, new_password: str):
        self.auth.update_user_password(id_token, new_password)

    def send_verification_email(self, id_token: str):
        self.auth.send_email_verification(id_token)
