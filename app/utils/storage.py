from pymongo import MongoClient
from gridfs import GridFS
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['BG_DB']
fs = GridFS(db)

async def save_file_to_db(file):
    """
    Saves an UploadFile to GridFS and returns the file_id
    """
    content = await file.read()
    file_id = fs.put(content, filename=file.filename)
    return str(file_id)
    
def get_file_from_db(file_id):
    """
    Returns bytes of file stored in GridFS
    """
    from bson import ObjectId
    try:
        file_data = fs.get(ObjectId(file_id))
        return file_data.read(), file_data.filename
    except Exception:
        return None, None
