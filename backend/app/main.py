from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from fastapi.staticfiles import StaticFiles
import os

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

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
