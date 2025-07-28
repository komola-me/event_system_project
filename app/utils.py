from passlib.context import CryptContext
from jose import jwt
from datetime import UTC, datetime, timedelta

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expires_delta: float | None = None):
    delta = (
        timedelta(minutes=expires_delta)
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    expire_time = datetime.now(UTC) + delta
    data.update({"exp": expire_time})

    jwt_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return jwt_token


def generate_confirmation_token(email):
    # data will be encoded to jwt token
    payload = {
        "email": email,
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)