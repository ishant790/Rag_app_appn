from fastapi import FastAPI, Depends
from pydantic import BaseModel
import time
from dotenv import load_dotenv
from services.loader import load_documents
from services.retriever import create_retrieval_components
from services.qa_chain import create_qa_chain
from config import get_config

load_dotenv()

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question: QuestionRequest, config: dict = Depends(get_config)):
    all_docs = load_documents(config["pdf_path"], config["user_agent"])
    retriever = create_retrieval_components(all_docs, config["google_api_key"])
    qa_chain = create_qa_chain(config["groq_api_key"], retriever)

    start = time.process_time()
    response = qa_chain.invoke({'input': question.question})
    end = time.process_time() - start

    return {"answer": response['answer'], "response_time": end}

@app.get("/reload")
async def reload_documents(config: dict = Depends(get_config)):
    try:
        _ = load_documents(config["pdf_path"], config["user_agent"])
        return {"message": "Documents reloaded successfully!"}
    except Exception as e:
        return {"error": str(e)}