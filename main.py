from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from routes.auth_routes import router as auth_router
from routes.chat_routes import router as chat_router
from routes.upload_routes import router as upload_router

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="SESSION_SECRET_KEY")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
