from fastapi import APIRouter, Depends
from app.dependency import current_user_dep
from app.models.models import User
from app.schemas.auth import UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def read_profile(current_user: current_user_dep):
    return current_user