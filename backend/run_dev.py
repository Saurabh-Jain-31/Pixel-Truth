#!/usr/bin/env python3
"""
Run development servers for frontend and backend
"""
import os
import subprocess
import sys
import threading
import time

def run_backend():
    """Run the FastAPI backend"""
    print("🐍 Starting FastAPI backend on port 5000...")
    os.system("python start.py")

def run_frontend():
    """Run the Vite frontend development server"""
    print("⚛️ Starting Vite frontend on port 3000...")
    time.sleep(2)  # Wait a bit for backend to start
    os.system("npm run dev")

def main():
    print("🚀 Starting Pixel-Truth Development Environment")
    print("=" * 50)
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:3000")
    print("API Docs: http://localhost:5000/docs")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("package.json"):
        print("❌ package.json not found. Make sure you're in the backend directory.")
        sys.exit(1)
    
    # Install dependencies if needed
    if not os.path.exists("node_modules"):
        print("📦 Installing frontend dependencies...")
        os.system("npm install")
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Start frontend (this will block)
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Development servers stopped")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()