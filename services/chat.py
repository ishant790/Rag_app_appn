from fastapi import APIRouter, Request, Form, Query
from services.loader import load_documents
from services.retriever import create_retrieval_components
from services.qa_chain import create_qa_chain
from config import get_config
from services.state import qa_chains_store  # import global chain store for question answer chain

router = APIRouter()

@router.post("/start_chat")
async def start_chat(request: Request, pdf_name: str = Form(...), api_key: str = Form(...), chat_id: str = Form(...)):
    config = get_config()
    pdf_path = request.session.get("pdfs", {}).get(pdf_name)
    if not pdf_path:
        return {"error": "PDF not found in session."}

    docs = load_documents(pdf_path, config["user_agent"])
    retriever = create_retrieval_components(docs, config["google_api_key"])
    qa_chain = create_qa_chain(api_key, retriever)

    # Save chain object in global store only
    qa_chains_store[chat_id] = qa_chain

    # Storing minimal data in session
    request.session.setdefault("chats", {})[chat_id] = {
        "pdf": pdf_name,
        "api_key": api_key,
        "messages": []
    }
    return {"message": f"Chat '{chat_id}' started."}

@router.post("/chat")
async def chat(request: Request, chat_id: str = Form(...), question: str = Form(...)):
    chats = request.session.get("chats", {})
    chat_data = chats.get(chat_id)
    if not chat_data:
        return {"error": "Chat session not found."}

    qa_chain = qa_chains_store.get(chat_id)
    if not qa_chain:
        return {"error": "QA chain not found for this chat."}

    response = qa_chain.invoke({"input": question})
    chat_data["messages"].append({"question": question, "answer": response['answer']})

    return {"chat_id": chat_id, "answer": response['answer'], "history": chat_data["messages"]}

@router.get("/chat_history")
async def get_chat_history(request: Request, chat_id: str = Query(...)):
    chats = request.session.get("chats", {})
    chat_data = chats.get(chat_id)
    if not chat_data:
        return {"error": "Chat session not found."}
    return {"chat_id": chat_id, "history": chat_data.get("messages", [])}
