
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
import time
from datetime import datetime

app = FastAPI(title="Pixel-Truth API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
os.makedirs("uploads", exist_ok=True)

# Serve static files if dist exists
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse("dist/index.html")
    
    @app.get("/{path:path}")
    async def serve_spa(path: str):
        if path.startswith("api/"):
            return JSONResponse({"error": "API endpoint not found"})
        return FileResponse("dist/index.html")

# Basic API endpoints
@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Pixel-Truth API is running"}

@app.get("/api/auth/test")
async def test_connection():
    return {"status": "connected", "message": "Backend is running"}

# Mock authentication endpoints (for demo)
@app.post("/api/auth/register")
async def register():
    return {
        "token": "demo_token_123",
        "user": {
            "id": "demo_user_id",
            "username": "demo_user",
            "email": "demo@example.com",
            "plan": "free",
            "analysis_count": 0,
            "monthly_analysis_limit": 10
        }
    }

@app.post("/api/auth/login")
async def login():
    return {
        "token": "demo_token_123", 
        "user": {
            "id": "demo_user_id",
            "username": "demo_user",
            "email": "demo@example.com",
            "plan": "free",
            "analysis_count": 0,
            "monthly_analysis_limit": 10
        }
    }

@app.get("/api/auth/me")
async def get_me():
    return {
        "id": "demo_user_id",
        "username": "demo_user",
        "email": "demo@example.com",
        "plan": "free",
        "analysis_count": 0,
        "monthly_analysis_limit": 10
    }

# File upload endpoint (connects to frontend)
@app.post("/api/upload")
async def upload_file(image: UploadFile = File(...)):
    """Upload file endpoint that frontend expects"""
    
    # Validate file type
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    file_ext = os.path.splitext(image.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_extensions}")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    unique_filename = f"{file_id}{file_ext}"
    
    # Save file
    file_path = os.path.join("uploads", unique_filename)
    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)
    
    return {
        "filename": unique_filename,
        "original_name": image.filename,
        "size": len(content),
        "mimetype": image.content_type,
        "upload_id": file_id
    }

# Analysis endpoint (connects to frontend)
@app.post("/api/analysis/analyze")
async def analyze_image(filename: str = Form(...), original_name: str = Form(...)):
    """Analyze uploaded image - connects to frontend"""
    
    file_path = os.path.join("uploads", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Simulate AI analysis (replace with actual AI model later)
    import random
    time.sleep(2)  # Simulate processing time
    
    predictions = ["authentic", "ai_generated", "manipulated"]
    prediction = random.choice(predictions)
    confidence = random.uniform(0.7, 0.95)
    
    # Mock analysis result
    analysis_result = {
        "analysis_id": str(uuid.uuid4()),
        "prediction": prediction,
        "confidence_score": confidence,
        "processing_time": 2.1,
        "metadata": {
            "exif_anomalies": {
                "missing_camera_info": prediction == "ai_generated",
                "unusual_dimensions": prediction == "ai_generated",
                "suspicious_software": False
            },
            "quality_metrics": {
                "sharpness": random.uniform(800, 1200),
                "noise_level": random.uniform(5, 25),
                "brightness": random.uniform(0.3, 0.8)
            }
        },
        "exif_data": {
            "format": "JPEG",
            "size": [1024, 768],
            "make": "Canon" if prediction == "authentic" else None
        },
        "status": "completed"
    }
    
    return analysis_result

# History endpoint
@app.get("/api/history")
async def get_history():
    """Get analysis history"""
    # Mock history data
    return {
        "analyses": [
            {
                "id": "analysis_1",
                "type": "image",
                "filename": "sample1.jpg",
                "prediction": "authentic",
                "confidence_score": 0.89,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "analysis_2", 
                "type": "image",
                "filename": "sample2.png",
                "prediction": "ai_generated",
                "confidence_score": 0.92,
                "created_at": datetime.now().isoformat()
            }
        ],
        "total_count": 2,
        "page": 1,
        "page_size": 20
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
