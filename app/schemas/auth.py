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


class LoginInput(BaseModel):
    email: EmailStr
    hashed_password: str


class TokenIn(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"