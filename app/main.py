from fastapi import FastAPI
from app.routes import health, upload, removebg, preview, download

app = FastAPI(title="Background Remover API")

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(removebg.router)
app.include_router(preview.router)
app.include_router(download.router)

@app.get("/")
async def root():
    return {"message": "Background Remover API Running"}
