from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    GOOGLE_API_KEY: str
    GROQ_API_KEY: str
    USER_AGENT: str
    SESSION_SECRET_KEY: str = "fallback-secret"

    class Config:
        env_file = ".env"
settings = Settings()