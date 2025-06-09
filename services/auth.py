from passlib.context import CryptContext
from fastapi import HTTPException
from services.db import create_user, get_user_by_username
from schema.auth import UserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def register_user(user_data: UserRegister):
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    hashed_pwd = hash_password(user_data.password)
    await create_user(user_data.username, user_data.email, hashed_pwd)

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user