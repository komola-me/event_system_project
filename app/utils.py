from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import UTC, datetime, timedelta

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, EMAIL_CONFIRM_EXPIRE_MINUTES

# pwd_context = CryptContext(schemes=["bcrypt"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_in_minutes: float | None = None):
    delta = (
        timedelta(minutes=expires_in_minutes)
        if expires_in_minutes
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    expire_time = datetime.now(UTC) + delta
    data.update({"exp": expire_time})

    jwt_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return jwt_token


def generate_confirmation_token(email: str) -> str:
    return create_jwt_token({"sub": email}, expires_in_minutes=EMAIL_CONFIRM_EXPIRE_MINUTES)


def decode_confirmation_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub") # return email
    except JWTError:
        raise ValueError("Invalid or expired confirmation token")