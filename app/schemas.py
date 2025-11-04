from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrderCreate(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class OrderUpdate(BaseModel):
    item_name: Optional[str] = Field(None, min_length=1, max_length=200)
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    item_name: str
    quantity: int
    price: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
