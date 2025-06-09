from fastapi import APIRouter, HTTPException, status
from schema.auth import UserRegister, UserLogin
from services.auth import register_user, authenticate_user
from utils.jwt_helper import create_access_token
from services.db import get_user_by_username

router = APIRouter()

@router.post("/register")
async def register(user_data: UserRegister):
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    await register_user(user_data)
    return {"message": "User registered successfully."}

@router.post("/login")
async def login(user_data: UserLogin):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    token = create_access_token({"sub": user_data.username})
    return {"access_token": token, "token_type": "bearer"}
