import uuid
from fastapi import APIRouter, UploadFile, File
from app.utils.storage import save_file

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = await save_file(file, filename)
    return {"file_path": path}
