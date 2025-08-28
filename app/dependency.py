from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from datetime import datetime
from jose import jwt, JWTError


from app.database import SessionLocal
from app.models.models import User
from app.config import SECRET_KEY, ALGORITHM

def get_db():
    db = SessionLocal()
    try:
        yield db # allows injection of db session into route
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# oauth2_scheme = HTTPBearer()


db_dep = Annotated[Session, Depends(get_db)]
oauth2_dep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(db: db_dep, token: oauth2_dep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials.", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True},)

        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise credentials_exception
        return user

    except JWTError as err:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from err
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Refresh token has expired!") from err


current_user_dep = Annotated[User, Depends(get_current_user)]

async def pagination_dependency(
        q: str | None = None,
        offset: int = 0,
        limit: int = 100,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        sort_by: str | None = None):
    return {"q": q, "offset": offset, "limit": limit,
            "date_from": date_from, "date_to": date_to, "sort_by": sort_by}

pagination_dep = Annotated[dict, Depends(pagination_dependency)]