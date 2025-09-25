import os
from fastapi import UploadFile

UPLOAD_DIR = "static/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file(file: UploadFile, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return file_path
