# TODO: Pydantic schemas - UserCreate, UserResponse, LoginRequest, Token, TransactionCreate, TransactionResponse, HoldingResponse
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Literal


# User Schemas
class UserBase(BaseModel):
    username: str= Field(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str= Field(min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True #so i could use this with sqlalchemy stuff

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Transaction Schemas
class TransactionBase(BaseModel):
    symbol: str= Field(min_length=1, max_length=10)
    type: Literal["BUY", "SELL"]
    quantity: float= Field(gt=0)
    price: float= Field(gt=0)
    @field_validator("symbol")
    def sanitize_txt(cls, v):
        return v.upper().strip()

class TransactionCreate(TransactionBase):
    date: datetime | None = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    date: datetime
    class Config:
        from_attributes = True

# Holding Schema
class HoldingResponse(BaseModel):
    symbol: str
    total_quantity: float
    average_price: float
    total_cost: float



