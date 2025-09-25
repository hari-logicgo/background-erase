import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/download")
async def download_file(filepath: str):
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=os.path.basename(filepath))
    return {"error": "File not found"}
