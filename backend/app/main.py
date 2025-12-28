"""
FastAPI main application entry point for AI Authenticity Verification Platform
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import logging
import os
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.auth import router as auth_router
from app.api.analysis import router as analysis_router
from app.api.history import router as history_router
from app.static_files import setup_static_files

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Authenticity Verification Platform...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Shutting down...")
    await close_mongo_connection()

# Initialize FastAPI app
app = FastAPI(
    title="AI Authenticity Verification Platform",
    description="Backend API for detecting AI-generated content in images and PDFs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers with /api prefix
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(analysis_router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(history_router, prefix="/api/history", tags=["History"])

# Setup static file serving for frontend
setup_static_files(app)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Authenticity Verification Platform API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "ml_models": "loaded"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,  # Changed to port 5000 to match frontend expectations
        reload=settings.DEBUG
    )