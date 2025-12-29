#!/usr/bin/env python3
"""
Test script to verify your Render deployment is working
"""
import requests
import json

SERVER_URL = "https://pixel-truth.onrender.com"

def test_render_server():
    print("🧪 Testing Pixel-Truth Render Deployment...")
    print(f"🌐 Server URL: {SERVER_URL}")
    print()
    
    # Test 1: Basic connection
    try:
        print("1️⃣ Testing basic connection...")
        response = requests.get(f"{SERVER_URL}/", timeout=30)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Test 2: Health check
    try:
        print("2️⃣ Testing health endpoint...")
        response = requests.get(f"{SERVER_URL}/api/health", timeout=30)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
    
    # Test 3: Auth test
    try:
        print("3️⃣ Testing auth endpoint...")
        response = requests.get(f"{SERVER_URL}/api/auth/test", timeout=30)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Auth test failed: {e}")
    
    # Test 4: Login test
    try:
        print("4️⃣ Testing login...")
        login_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        response = requests.post(f"{SERVER_URL}/api/auth/login", 
                               json=login_data, 
                               timeout=30)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Login test failed: {e}")
    
    print("🎉 Render server tests completed!")
    print()
    print("📋 Next steps:")
    print("1. Update frontend configuration to use Render URL")
    print("2. Enable GitHub Pages in repository settings")
    print("3. Test the complete flow")
    print(f"4. GitHub Pages: https://saurabh-jain-31.github.io/Pixel-Truth-GDG/")

if __name__ == "__main__":
    test_render_server()