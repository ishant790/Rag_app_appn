# services/upload.py

import os
from fastapi import APIRouter, UploadFile, File
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = "uploads"

# Ensure the uploads directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# This global variable will track the latest uploaded file
latest_uploaded_path = None

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global latest_uploaded_path

    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    latest_uploaded_path = file_path

    return {
        "message": f"File '{file.filename}' uploaded successfully.",
        "stored_as": filename,
        "path": file_path
    }
