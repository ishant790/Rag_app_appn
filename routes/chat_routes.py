from fastapi import APIRouter, Depends, HTTPException
from schema.chat import ChatRequest, StartChatRequest
from services.chat import start_chat_service, chat_service
from utils.jwt_helper import get_logged_in_user

router = APIRouter()

@router.post("/start")
async def start_chat(request: StartChatRequest, username: str = Depends(get_logged_in_user)):
    return await start_chat_service(request, username)

@router.post("/")
async def chat(request: ChatRequest, username: str = Depends(get_logged_in_user)):
    response = await chat_service(request, username)
    if not response:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    return response

