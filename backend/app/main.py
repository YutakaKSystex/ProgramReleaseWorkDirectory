from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
from pathlib import Path

from app.routers import auth, users, folders, documents, approval_forms, approval_routes, applications

app = FastAPI(title="Document Management System API")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(folders.router)
app.include_router(documents.router)
app.include_router(approval_forms.router)
app.include_router(approval_routes.router)
app.include_router(applications.router)

os.makedirs("uploads", exist_ok=True)
os.makedirs("frontend", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_frontend(request: Request, full_path: str):
    if full_path.startswith("api/") or full_path == "healthz" or full_path.startswith("uploads/"):
        return {"detail": "Not Found"}
    
    index_path = Path("frontend/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    else:
        return HTMLResponse("<html><body><h1>Frontend not found</h1><p>Please build and copy the frontend files to the 'frontend' directory.</p></body></html>")
