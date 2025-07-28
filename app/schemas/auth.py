from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    username: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime


class TokenIn():
    refresh_token: str


class TokenOut():
    access_token: str
    refresh_token: str
    token_type: str