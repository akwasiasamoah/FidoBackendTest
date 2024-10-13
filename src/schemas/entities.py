from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime
from src.utils.encryption import encrypt, decrypt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    transaction = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    full_name = Column(String, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    transaction_amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  

    user = relationship("User", back_populates="transaction")



@property
def encrypted_full_name(self):
    return encrypt(self.full_name)

@encrypted_full_name.setter
def encrypted_full_name(self, value):
    self.full_name = decrypt(value)
