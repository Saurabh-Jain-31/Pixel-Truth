#!/usr/bin/env python3
"""
Test script to verify your deployed server is working
"""
import requests
import json

SERVER_URL = "http://74.220.48.0:5000"

def test_server():
    print("🧪 Testing Pixel-Truth Server Connection...")
    print(f"🌐 Server URL: {SERVER_URL}")
    print()
    
    # Test 1: Basic connection
    try:
        print("1️⃣ Testing basic connection...")
        response = requests.get(f"{SERVER_URL}/", timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Test 2: Health check
    try:
        print("2️⃣ Testing health endpoint...")
        response = requests.get(f"{SERVER_URL}/api/health", timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
    
    # Test 3: Auth test
    try:
        print("3️⃣ Testing auth endpoint...")
        response = requests.get(f"{SERVER_URL}/api/auth/test", timeout=10)
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
                               timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Login test failed: {e}")
    
    print("🎉 Server tests completed!")
    print()
    print("📋 Next steps:")
    print("1. Make sure your server is running on port 5000")
    print("2. Check firewall settings allow port 5000")
    print("3. Visit your GitHub Pages site and try logging in")
    print(f"4. GitHub Pages: https://saurabh-jain-31.github.io/Pixel-Truth-GDG/")

if __name__ == "__main__":
    test_server()