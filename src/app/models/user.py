from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Fields for email verification
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True, unique=True)
    verification_expires = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def set_verification_code(self, code: str, expires_in: int = 3600):
        self.verification_code = code
        self.verification_expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)    
        