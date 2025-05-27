from fastapi import APIRouter, Request, Form
from services.state import session_store
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/session")
async def view_session(request: Request):
    return request.session

@router.post("/reset")
async def reset_session(request: Request):
    request.session.clear()
    return {"message": "Session reset."}

@router.post("/start-chat")
async def start_chat(request: Request, chat_id: str = Form(...), api_key: str = Form(...)):
    try:
        logger.info(f"Starting chat with ID: {chat_id}")
        request.session['chat_id'] = chat_id
        request.session['api_key'] = api_key
        session_store[chat_id] = {
            "api_key": api_key,
            "messages": []
        }
        logger.info(f"Session store updated for chat_id: {chat_id}")
        return {"message": "Chat started.", "chat_id": chat_id}
    except Exception as e:
        logger.error(f"Error starting chat: {e}")
        return {"error": "Internal Server Error", "details": str(e)}

