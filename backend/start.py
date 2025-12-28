#!/usr/bin/env python3
"""
Development startup script
"""
import uvicorn
import os
from app.core.config import settings

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("datasets", exist_ok=True)
    os.makedirs("ml/models", exist_ok=True)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,  # Changed to port 5000 to match frontend expectations
        reload=settings.DEBUG,
        log_level="info"
    )