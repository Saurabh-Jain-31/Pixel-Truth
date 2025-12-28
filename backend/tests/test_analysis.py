"""
Tests for analysis endpoints
"""
import pytest
from httpx import AsyncClient
from app.main import app
import io
from PIL import Image

@pytest.mark.asyncio
async def test_image_analysis_unauthorized():
    """Test image analysis without authentication"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        response = await ac.post("/analyze/image", files={
            "file": ("test.jpg", img_bytes, "image/jpeg")
        })
    
    assert response.status_code == 403  # Unauthorized

@pytest.mark.asyncio
async def test_invalid_file_type():
    """Test upload with invalid file type"""
    # First get auth token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register and login
        await ac.post("/auth/register", json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword123"
        })
        
        login_response = await ac.post("/auth/login", json={
            "email": "test2@example.com",
            "password": "testpassword123"
        })
        
        token = login_response.json()["access_token"]
        
        # Try to upload invalid file type
        response = await ac.post("/analyze/image", 
            files={"file": ("test.txt", b"not an image", "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    assert response.status_code == 400