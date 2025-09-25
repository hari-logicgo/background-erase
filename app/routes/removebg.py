import uuid
from fastapi import APIRouter, UploadFile, File
from app.utils.storage import save_file
from app.utils.processor import remove_bg

router = APIRouter()

@router.post("/removebg")
async def remove_background(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = await save_file(file, filename)
    result = remove_bg(path)
    return {"processed_file": result}
