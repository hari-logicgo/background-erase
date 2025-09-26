import os
import uuid
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from gradio_client import Client, handle_file

# Initialize FastAPI
app = FastAPI()

# Initialize Hugging Face Client
client = Client("LogicGoInfotechSpaces/background-remover")

# Create static folder to store files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Upload source image
@app.post("/source")
async def upload_source(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4()) + "_" + file.filename
    file_path = os.path.join("static", file_id)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"source_path": f"/static/{file_id}"}

# Background remover (protected)
# Background remover (protected)
@app.post("/bg-remove")
async def bg_remove(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):
    # Token check
    if authorization != "Bearer logicgo@123":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Save uploaded file
    file_id = str(uuid.uuid4()) + "_" + file.filename
    input_path = os.path.join("static", file_id)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Call Hugging Face Space via gradio_client
    result_path = client.predict(
        f=handle_file(input_path),
        api_name="/png"
    )

    # Copy result into static folder
    output_id = f"bgremoved_{file_id}"
    output_path = os.path.join("static", output_id)
    os.replace(result_path, output_path)

    return {
        "bg_removed_path": f"/static/{output_id}",
        "filename": output_id   # 👈 Added this line
    }


# Preview processed image
@app.get("/preview/{filename}")
def preview(filename: str):
    file_path = os.path.join("static", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

# Download processed image
@app.get("/download/{filename}")
def download(filename: str):
    file_path = os.path.join("static", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
