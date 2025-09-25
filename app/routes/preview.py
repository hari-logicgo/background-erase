from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.utils.storage import get_file_from_db

router = APIRouter()

@router.get("/preview/{file_id}")
def preview_image(file_id: str):
    content, filename = get_file_from_db(file_id)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return StreamingResponse(BytesIO(content), media_type="image/png")
