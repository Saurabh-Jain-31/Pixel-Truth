#!/usr/bin/env python3
"""
Debug the API connection issue
"""
import requests
import time

def test_multiple_endpoints():
    """Test different possible endpoints"""
    
    endpoints_to_test = [
        "https://pixel-truth.onrender.com",
        "https://pixel-truth.onrender.com/",
        "https://pixel-truth.onrender.com/api/health",
        "https://pixel-truth.onrender.com/api/auth/test",
    ]
    
    print("🔍 Testing Multiple Endpoints...")
    print("=" * 50)
    
    for endpoint in endpoints_to_test:
        print(f"\n🧪 Testing: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=60)
            print(f"   ✅ Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print(f"   📄 Response: {json_data}")
                except:
                    print(f"   📄 Response: {response.text[:200]}...")
            else:
                print(f"   📄 Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout - Service might be cold starting")
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error - Service might be down")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🔧 Troubleshooting Steps:")
    print("1. Check if your Render service is running")
    print("2. Look at Render service logs for errors")
    print("3. Verify the service URL is correct")
    print("4. Check if the service is sleeping (free tier)")
    print("5. Try visiting the URL directly in browser")

def test_github_pages_api_calls():
    """Test what happens when we make API calls from GitHub Pages perspective"""
    
    print("\n🌐 Testing GitHub Pages API Behavior...")
    print("=" * 50)
    
    # This simulates what the frontend is trying to do
    github_api_url = "https://saurabh-jain-31.github.io/api/auth/register"
    
    print(f"🧪 Testing GitHub Pages API URL: {github_api_url}")
    try:
        response = requests.post(github_api_url, json={"test": "data"}, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error (expected): {e}")
    
    print("\n✅ This confirms the issue:")
    print("   • Frontend is trying to call GitHub Pages for API")
    print("   • GitHub Pages doesn't have API endpoints")
    print("   • We need to redirect API calls to Render")

if __name__ == "__main__":
    test_multiple_endpoints()
    test_github_pages_api_calls()
    
    print("\n🎯 Solution:")
    print("1. Enable GitHub Pages in repository settings")
    print("2. Wait for Render service to wake up")
    print("3. API redirect script will handle the routing")
    print("4. Test the complete flow")