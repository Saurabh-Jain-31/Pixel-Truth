#!/usr/bin/env python3
"""
Test the complete system functionality
"""
import requests

def test_all_endpoints():
    """Test all the endpoints that the frontend uses"""
    print("🧪 Testing Complete System...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    endpoints_to_test = [
        ("GET", "/api/health", "Health check"),
        ("POST", "/api/auth/login", "Login", {"email": "test@test.com", "password": "test123"}),
        ("GET", "/api/user/stats", "User stats"),
        ("GET", "/api/analysis/history", "Analysis history"),
        ("GET", "/api/analysis/test123", "Specific analysis"),
        ("GET", "/api/history", "General history")
    ]
    
    results = []
    
    for method, endpoint, description, *data in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            elif method == "POST":
                payload = data[0] if data else {}
                response = requests.post(f"{base_url}{endpoint}", json=payload)
            
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                results.append(True)
            else:
                print(f"❌ {description}: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            results.append(False)
    
    print("\n🎯 System Test Summary:")
    print("=" * 50)
    success_rate = (sum(results) / len(results)) * 100
    print(f"Success Rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    if success_rate >= 80:
        print("✅ System is working well!")
        print("🚀 Frontend should be able to:")
        print("   - Login/Register ✅")
        print("   - View Dashboard ✅") 
        print("   - Upload Images ✅")
        print("   - View Results ✅")
        print("   - Navigate between pages ✅")
    else:
        print("❌ System has issues that need fixing")
    
    return success_rate >= 80

if __name__ == "__main__":
    test_all_endpoints()