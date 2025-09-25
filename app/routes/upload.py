from fastapi import APIRouter, UploadFile, File
from app.utils.storage import save_file_to_db

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads image to MongoDB GridFS and returns file_id
    """
    file_id = await save_file_to_db(file)
    return {"file_id": file_id, "filename": file.filename}
