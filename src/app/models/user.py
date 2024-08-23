# app/models/user.py
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)  # New name field
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Fields for email verification
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True, unique=True)
    token_expiration = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Create an index for token expiration for efficient queries
    __table_args__ = (
        Index('ix_verification_token', 'verification_token'),
        Index('ix_token_expiration', 'token_expiration'),
    )

    def set_verification_token(self, token: str, expires_in: int = 3600):
        self.verification_token = token
        self.token_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
