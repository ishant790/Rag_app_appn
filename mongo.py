from motor.motor_asyncio import AsyncIOMotorClient
from config.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

users_collection = db["users"]
chats_collection = db["chats"]