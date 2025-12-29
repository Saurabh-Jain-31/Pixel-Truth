#!/usr/bin/env python3
"""
Script to check GitHub Pages status and provide setup instructions
"""
import requests
import json

def check_github_pages():
    print("🔍 Checking GitHub Pages Status...")
    print()
    
    # Check if GitHub Pages is accessible
    github_pages_url = "https://saurabh-jain-31.github.io/Pixel-Truth-GDG/"
    
    try:
        print(f"📡 Testing GitHub Pages URL: {github_pages_url}")
        response = requests.get(github_pages_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ GitHub Pages is working!")
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        elif response.status_code == 404:
            print("❌ GitHub Pages shows 404 - Site not found")
            print("   This means GitHub Pages is not enabled in repository settings")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to GitHub Pages")
        print("   This usually means GitHub Pages is not enabled")
    except Exception as e:
        print(f"❌ Error checking GitHub Pages: {e}")
    
    print()
    print("📋 To fix GitHub Pages '404 There isn't a GitHub Pages site here' error:")
    print()
    print("1. Go to your repository: https://github.com/Saurabh-Jain-31/Pixel-Truth-GDG")
    print("2. Click on 'Settings' tab")
    print("3. Scroll down to 'Pages' section in the left sidebar")
    print("4. Under 'Source', select 'Deploy from a branch'")
    print("5. Choose 'main' or 'master' branch")
    print("6. Choose '/ (root)' folder")
    print("7. Click 'Save'")
    print()
    print("⏱️  It may take a few minutes for GitHub Pages to deploy")
    print("🌐 Your site will be available at: https://saurabh-jain-31.github.io/Pixel-Truth-GDG/")
    print()
    
    # Check if files are properly set up
    print("📁 Checking required files for GitHub Pages...")
    
    required_files = [
        "index.html",
        "404.html", 
        ".nojekyll",
        "assets/index-cce1568a.js",
        "assets/index-b2814743.css"
    ]
    
    for file_path in required_files:
        if file_path.startswith("assets/"):
            # Check if assets directory exists
            import os
            if os.path.exists(file_path):
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path} - Missing!")
        else:
            import os
            if os.path.exists(file_path):
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path} - Missing!")

if __name__ == "__main__":
    check_github_pages()