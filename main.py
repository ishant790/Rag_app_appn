from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware 

from services.upload import router as upload_router
from services.chat import router as chat_router
from services.session_routes import router as session_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(session_router)