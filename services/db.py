from datetime import datetime, timezone
from bson.objectid import ObjectId
from mongo import users_collection, chats_collection  # import from mongo.py


async def create_user(username: str, email: str, hashed_password: str):
    await users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })


async def get_user_by_username(username: str):
    return await users_collection.find_one({"username": username})


async def save_message_to_db(chat_id: str, username: str, question: str, answer: str):
    await chats_collection.insert_one({
        "chat_id": chat_id,
        "username": username,
        "question": question,
        "answer": answer,
        "timestamp": datetime.now(timezone.utc)
    })


async def get_chat_history_from_db(chat_id: str, username: str):
    cursor = chats_collection.find({"chat_id": chat_id, "username": username}).sort("timestamp")
    return [{"question": r["question"], "answer": r["answer"]} async for r in cursor]

async def chat_exists_in_db(chat_id: str, username: str) -> bool:
    count = await chats_collection.count_documents({"chat_id": chat_id, "username": username})
    return count > 0
