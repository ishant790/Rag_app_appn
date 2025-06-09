from pydantic import BaseModel

class StartChatRequest(BaseModel):
    pdf_name: str
    chat_id: str
    api_key: str

class ChatRequest(BaseModel):
    chat_id: str
    question: str