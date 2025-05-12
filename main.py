from fastapi import FastAPI, Depends
from pydantic import BaseModel
import time
from dotenv import load_dotenv
from services.loader import load_documents
from services.retriever import create_retrieval_components
from services.qa_chain import create_qa_chain
from config import get_config
import os
from services.upload import router as upload_router
from services import state  # Import shared state

load_dotenv()

app = FastAPI()
qa_history = []  # Store all questions and answers

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question: QuestionRequest, config: dict = Depends(get_config)):
    if not state.latest_uploaded_path or not os.path.exists(state.latest_uploaded_path):
        return {"error": "No uploaded PDF found. Please upload a file first using /upload."}

    all_docs = load_documents(state.latest_uploaded_path, config["user_agent"])
    retriever = create_retrieval_components(all_docs, config["google_api_key"])
    qa_chain = create_qa_chain(config["groq_api_key"], retriever)

    start = time.process_time()
    response = qa_chain.invoke({'input': question.question})
    end = time.process_time() - start

    qa_history.append({
        "question": question.question,
        "answer": response['answer'],
        "response_time": end
    })

    return {"answer": response['answer'], "response_time": end}

@app.get("/reload")
async def reload_documents(config: dict = Depends(get_config)):
    try:
        _ = load_documents(state.latest_uploaded_path, config["user_agent"])
        return {"message": "Documents reloaded successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/history")
async def get_history():
    return {"history": qa_history}

# Include the router for uploading files
app.include_router(upload_router)
