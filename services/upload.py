<<<<<<< HEAD
import os
from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from services import state  # Shared state

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    state.latest_uploaded_path = file_path  # Save to shared state
    return {
        "message": f"File '{file.filename}' uploaded successfully.",
        "stored_as": filename,
        "path": file_path
    }
=======
import os
from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from services import state  # Shared state

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    state.latest_uploaded_path = file_path  # Save to shared state
    return {
        "message": f"File '{file.filename}' uploaded successfully.",
        "stored_as": filename,
        "path": file_path
    }
>>>>>>> 26fd72653a205e6daaffecbc9bfa069dfca8bbd9
