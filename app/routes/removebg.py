import uuid
from fastapi import APIRouter, Header, HTTPException
from io import BytesIO
import base64
from app.utils.storage import get_file_from_db, save_file_to_db
from app.utils.processor import remove_bg
from app.config import AUTH_TOKEN

router = APIRouter()

def verify_token(authorization: str = Header(...)):
    """
    Check Bearer token
    """
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/remove-bg")
async def remove_background(file_id: str, authorization: str = Header(...)):
    """
    Removes background of an image stored in GridFS and saves the processed image back to GridFS.
    Returns processed_file_id.
    """
    # Verify token
    verify_token(authorization)

    # Get original image from GridFS
    content, filename = get_file_from_db(file_id)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")

    # Save temporary file locally
    temp_input_path = f"/tmp/{uuid.uuid4()}_{filename}"
    with open(temp_input_path, "wb") as f:
        f.write(content)

    # Call HF Space to remove background
    result = remove_bg(temp_input_path)

    # If result is base64 string, decode it
    if isinstance(result, str):
        if result.startswith("data:image"):
            result = result.split(",")[1]
        result_bytes = base64.b64decode(result)
    else:
        # Already bytes
        result_bytes = result

    # Save processed image to GridFS
    processed_file_id = await save_file_to_db(BytesIO(result_bytes))

    return {"processed_file_id": processed_file_id, "filename": f"processed_{filename}"}
