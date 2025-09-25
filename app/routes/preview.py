import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/preview")
async def preview_image(filepath: str):
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return {"error": "File not found"}
