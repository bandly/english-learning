from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: Optional[str] = None  # Optional password


class UserLogin(BaseModel):
    username: str
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login_at: Optional[datetime] = None
    settings: Optional[dict] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse