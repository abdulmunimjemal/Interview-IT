# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.auth_utils import get_password_hash
import uuid

def get_user(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        name=user.name  # Include name in the user creation
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: uuid.UUID, user: UserUpdate):
    db_user = get_user(db, user_id)
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    db_user.name = user.name  # Update name if provided
    db.commit()
    db.refresh(db_user)
    return db_user
