"""
Tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user():
    """Test user login"""
    # First register a user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpassword123"
        })
        
        # Then login
        response = await ac.post("/auth/login", json={
            "email": "login@example.com",
            "password": "testpassword123"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_login():
    """Test login with invalid credentials"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
    
    assert response.status_code == 401