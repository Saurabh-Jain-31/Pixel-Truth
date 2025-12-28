#!/usr/bin/env python3
"""
Simple startup script that handles common issues
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'motor', 'pymongo', 
        'pydantic-settings', 'python-jose', 'passlib',
        'email-validator', 'python-multipart'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        for package in missing:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])
    else:
        print("✅ All dependencies are installed")

def start_simple_server():
    """Start a simple FastAPI server without complex dependencies"""
    print("🚀 Starting Pixel-Truth Backend Server...")
    print("=" * 50)
    
    # Create a simple main.py that works
    simple_main = '''
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Pixel-Truth API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files if dist exists
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse("dist/index.html")
    
    @app.get("/{path:path}")
    async def serve_spa(path: str):
        if path.startswith("api/"):
            return JSONResponse({"error": "API endpoint not implemented yet"})
        return FileResponse("dist/index.html")

# Basic API endpoints
@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Pixel-Truth API is running"}

@app.get("/api/auth/test")
async def test_connection():
    return {"status": "connected", "message": "Backend is running"}

@app.post("/api/auth/register")
async def register():
    return {"message": "Registration endpoint - coming soon"}

@app.post("/api/auth/login")
async def login():
    return {"message": "Login endpoint - coming soon"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
'''
    
    # Write simple main
    with open('simple_main.py', 'w') as f:
        f.write(simple_main)
    
    print("✅ Simple server configuration created")
    print("🌐 Starting server on http://localhost:5000")
    print("📖 API docs available at http://localhost:5000/docs")
    print("=" * 50)
    
    # Start the server
    os.system("python simple_main.py")

def main():
    print("🔧 Pixel-Truth Simple Startup")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Start simple server
    start_simple_server()

if __name__ == "__main__":
    main()