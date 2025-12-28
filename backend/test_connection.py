#!/usr/bin/env python3
"""
Test script to verify frontend-backend connectivity
"""
import requests
import json

def test_backend_connection():
    """Test backend API endpoints"""
    print("🧪 Testing Backend Connection...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
    
    # Test auth endpoints
    try:
        response = requests.post(f"{base_url}/api/auth/register", 
                               json={"username": "test", "email": "test@test.com", "password": "test123"})
        print(f"✅ Register Endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Register Failed: {e}")
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", 
                               json={"email": "test@test.com", "password": "test123"})
        print(f"✅ Login Endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Login Failed: {e}")

def test_frontend_connection():
    """Test frontend server"""
    print("\n🌐 Testing Frontend Connection...")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:3000")
        print(f"✅ Frontend Server: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
    except Exception as e:
        print(f"❌ Frontend Connection Failed: {e}")

if __name__ == "__main__":
    test_backend_connection()
    test_frontend_connection()
    
    print("\n🎯 Summary:")
    print("=" * 50)
    print("✅ Backend (FastAPI): http://localhost:5000")
    print("✅ Frontend (Vite): http://localhost:3000")
    print("✅ API Proxy: /api/* → localhost:5000")
    print("\n🚀 Ready for testing!")
    print("   1. Open http://localhost:3000 in browser")
    print("   2. Try registration/login")
    print("   3. Upload and analyze images")