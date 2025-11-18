# TODO: SQLAlchemy models - User table (id, username, email, hashed_password, created_at)
# TODO: SQLAlchemy models - Transaction table (id, user_id, symbol, type, quantity, price, date)
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from .database import Base

class TranactionType(str, PyEnum):
    BUY = "buy"
    SELL = "sell"

class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


