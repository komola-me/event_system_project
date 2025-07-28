from fastapi import APIRouter, HTTPException

from app.models.models import User
from app.schemas.auth import UserCreate, UserRead
from app.dependency import db_dep
from app.utils import hash_password, verify_password, generate_confirmation_token, create_jwt_token
from jose import JWTError, jwt
from app.tasks import send_email
from app.config import FRONTEND_URL, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def register_user(db: db_dep, user: UserCreate):
    existing_user_by_email = db.query(User).filter(User.email == user.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already in use")

    existing_user_by_username = db.query(User).filter(User.username == user.username).first()
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username already in use")

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.hashed_password),
        is_admin=False,
        is_active=False,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = generate_confirmation_token(email=user.email)

    send_email.delay(
        to_email=new_user.email,
        subject="Confirmation of your registration to Event Management System",
        body=f"Please click the link to confirm your email: {FRONTEND_URL}/auth/confirm/{token}",
    )
    return {
        "detail": f"Confirmation email has been sent to {new_user.email}. Please confirm to finilize your registration.",
    }


@router.get("/confirm/{token}/")
async def confirm_email(db: db_dep, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token is invalid or expired")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"detail": "User already verified"}

    user.is_verified = True
    user.is_active = True
    db.commit()
    return {"detail": "Email successfully verified"}
