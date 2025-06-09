from fastapi import HTTPException
from services.loader import load_documents
from services.retriever import create_retrieval_components
from services.qa_chain import create_qa_chain
from services.state import qa_chains_store
from services.db import save_message_to_db, get_chat_history_from_db, chat_exists_in_db
from config.config import settings
import os

UPLOAD_DIR = "uploads"

async def start_chat_service(request, username: str):
    from schema.chat import StartChatRequest
    pdf_path = os.path.join(UPLOAD_DIR, request.pdf_name)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found.")
    
    # Rehydrate QA chain if server restarted
    if request.chat_id in qa_chains_store:
        return {"message": f"Chat session '{request.chat_id}' already active."}

    if await chat_exists_in_db(request.chat_id, username):
        docs = load_documents(pdf_path, settings.USER_AGENT)
        retriever = create_retrieval_components(docs, settings.GOOGLE_API_KEY)
        qa_chain = create_qa_chain(request.api_key, retriever)
        qa_chains_store[request.chat_id] = qa_chain
        return {"message": f"Chat session '{request.chat_id}' resumed."}

    # Fresh session
    docs = load_documents(pdf_path, settings.USER_AGENT)
    retriever = create_retrieval_components(docs, settings.GOOGLE_API_KEY)
    qa_chain = create_qa_chain(request.api_key, retriever)
    qa_chains_store[request.chat_id] = qa_chain

    return {"message": f"Chat session '{request.chat_id}' started."}


async def chat_service(request, username: str):
    qa_chain = qa_chains_store.get(request.chat_id)
    if not qa_chain:
        raise HTTPException(status_code=404, detail="QA chain not found")

    history_records = await get_chat_history_from_db(request.chat_id, username)
    history_text = "\n".join(
        [f"User: {h['question']}\nAssistant: {h['answer']}" for h in history_records]
    )

    response = qa_chain.invoke({
        "input": request.question,
        "context": history_text
    })

    answer = response["answer"]
    await save_message_to_db(request.chat_id, username, request.question, answer)

    return {"question": request.question, "answer": answer}
