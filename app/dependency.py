from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db # allows injection of db session into route
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


db_dep = Annotated[Session, Depends(get_db)]
oauth2_dep = Annotated[str, Depends(oauth2_scheme)]