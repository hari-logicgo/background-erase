import uuid
from io import BytesIO
from pymongo import MongoClient
from gridfs import GridFS
from app.config import MONGO_URI
from fastapi import UploadFile
from bson import ObjectId

client = MongoClient(MONGO_URI)
db = client['BG_DB']
fs = GridFS(db)

async def save_file_to_db(file: UploadFile | BytesIO):
    """
    Save UploadFile or BytesIO to GridFS and return file_id
    """
    if isinstance(file, UploadFile):
        # Always await read() for UploadFile
        content = await file.read()
        filename = file.filename
    else:
        # BytesIO
        file.seek(0)
        content = file.read()
        filename = f"{uuid.uuid4()}.png"

    # fs.put expects bytes or file-like object
    file_id = fs.put(BytesIO(content), filename=filename)
    return str(file_id)

def get_file_from_db(file_id: str):
    """
    Retrieve file bytes and filename from GridFS
    """
    try:
        file_data = fs.get(ObjectId(file_id))
        return file_data.read(), file_data.filename
    except Exception:
        return None, None
