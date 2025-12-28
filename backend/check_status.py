#!/usr/bin/env python3
"""
Check the status of both frontend and backend servers
"""
import requests
import time

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend: Running on http://localhost:5000")
            print("📖 API Docs: http://localhost:5000/docs")
            return True
    except:
        pass
    
    print("❌ Backend: Not running on http://localhost:5000")
    return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Running on http://localhost:3000")
            return True
    except:
        pass
    
    print("❌ Frontend: Not running on http://localhost:3000")
    return False

def main():
    print("🔍 Pixel-Truth Server Status Check")
    print("=" * 40)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    print("\n📊 Status Summary:")
    if backend_ok and frontend_ok:
        print("🎉 Both servers are running!")
        print("\n🚀 Access your application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:5000")
        print("   API Docs: http://localhost:5000/docs")
    elif backend_ok:
        print("⚠️ Backend running, but frontend not started")
        print("   Run: npm run dev")
    elif frontend_ok:
        print("⚠️ Frontend running, but backend not started")
        print("   Run: python simple_start.py")
    else:
        print("❌ Neither server is running")
        print("   Run: python simple_start.py (backend)")
        print("   Run: npm run dev (frontend)")

if __name__ == "__main__":
    main()