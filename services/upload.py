import os
from uuid import uuid4
from fastapi import APIRouter, Request, UploadFile, File

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    request.session.setdefault("pdfs", {})[filename] = file_path
    return {"message": f"Uploaded {file.filename}", "stored_as": filename}
