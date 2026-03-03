from http.client import HTTPException

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UserRepository
from src.models.users import UsersOrm


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password =  pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UserRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "ok"}