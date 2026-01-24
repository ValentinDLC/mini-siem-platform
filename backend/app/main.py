"""
Mini SIEM Platform - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.database import init_db
from backend.app.api.endpoints import router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Mini SIEM Platform for security monitoring"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    init_db()
    print(f"[*] {settings.project_name} v{settings.version} started")


@app.get("/")
def root():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
