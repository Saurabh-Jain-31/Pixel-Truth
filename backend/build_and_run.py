#!/usr/bin/env python3
"""
Build frontend and run the integrated application
"""
import os
import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Building and Running Pixel-Truth Platform")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("package.json"):
        print("❌ package.json not found. Make sure you're in the backend directory.")
        sys.exit(1)
    
    # Install frontend dependencies
    if not run_command("npm install", "Installing frontend dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Build frontend
    if not run_command("npm run build", "Building frontend"):
        print("❌ Failed to build frontend")
        sys.exit(1)
    
    # Check if dist directory was created
    if not os.path.exists("dist"):
        print("❌ Frontend build failed - dist directory not found")
        sys.exit(1)
    
    print("✅ Frontend built successfully!")
    print("📁 Built files are in the 'dist' directory")
    
    # Install Python dependencies
    print("\n🐍 Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️ Some Python dependencies may have failed to install")
        print("   The application may still work with existing packages")
    
    print("\n🎉 Build completed successfully!")
    print("\n🚀 Starting the integrated application...")
    print("   Frontend: React.js (served by FastAPI)")
    print("   Backend: FastAPI with AI detection")
    print("   Port: 5000")
    print("   URL: http://localhost:5000")
    
    print("\n" + "=" * 50)
    print("🌐 Application starting...")
    print("   Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start the application
    try:
        os.system("python start.py")
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()