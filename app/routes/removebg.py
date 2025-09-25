from fastapi import APIRouter, Header, HTTPException
from app.utils.storage import get_file_from_db, save_file_to_db
from app.utils.processor import remove_bg
from app.config import AUTH_TOKEN
import uuid
from PIL import Image
from io import BytesIO

router = APIRouter()

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/remove-bg")
async def remove_background(file_id: str, authorization: str = Header(...)):
    """
    Removes background of image stored in GridFS, saves processed image back to GridFS
    """
    verify_token(authorization)
    
    content, filename = get_file_from_db(file_id)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Save temporary file to local
    temp_input_path = f"/tmp/{uuid.uuid4()}_{filename}"
    with open(temp_input_path, "wb") as f:
        f.write(content)
    
    # Call HF Space to remove background
    result_bytes = remove_bg(temp_input_path)
    
    # Save processed image to GridFS
    processed_file_id = await save_file_to_db(BytesIO(result_bytes))
    
    return {"processed_file_id": processed_file_id, "filename": f"processed_{filename}"}
