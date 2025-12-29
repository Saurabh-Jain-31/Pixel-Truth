#!/usr/bin/env python3
"""
Wake up the Render service and test it
"""
import requests
import time

def wake_up_render():
    """Wake up the Render service from cold start"""
    
    render_url = "https://pixel-truth.onrender.com"
    
    print("🚀 Waking up Render service...")
    print(f"🌐 URL: {render_url}")
    print("⏰ This may take 30-60 seconds for cold start...")
    print()
    
    # Try multiple times with increasing timeout
    for attempt in range(3):
        print(f"🧪 Attempt {attempt + 1}/3...")
        
        try:
            # Start with a simple GET request
            response = requests.get(render_url, timeout=90)
            
            if response.status_code == 200:
                print("✅ Render service is awake!")
                print(f"   Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response: {data}")
                except:
                    print(f"   Response: {response.text[:200]}...")
                
                # Test API endpoints
                print("\n🧪 Testing API endpoints...")
                
                endpoints = ["/api/health", "/api/auth/test"]
                for endpoint in endpoints:
                    try:
                        api_response = requests.get(f"{render_url}{endpoint}", timeout=30)
                        print(f"   ✅ {endpoint}: {api_response.status_code}")
                        if api_response.status_code == 200:
                            try:
                                print(f"      📄 {api_response.json()}")
                            except:
                                print(f"      📄 {api_response.text[:100]}...")
                    except Exception as e:
                        print(f"   ❌ {endpoint}: {e}")
                
                return True
                
            else:
                print(f"   ⚠️ Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout on attempt {attempt + 1}")
            if attempt < 2:
                print("   🔄 Retrying in 10 seconds...")
                time.sleep(10)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            if attempt < 2:
                print("   🔄 Retrying in 10 seconds...")
                time.sleep(10)
    
    print("\n❌ Could not wake up Render service")
    print("🔧 Please check:")
    print("1. Render service is deployed and running")
    print("2. Service URL is correct")
    print("3. No errors in Render logs")
    print("4. Service hasn't exceeded free tier limits")
    
    return False

if __name__ == "__main__":
    success = wake_up_render()
    
    if success:
        print("\n🎉 Render service is ready!")
        print("✅ You can now test your GitHub Pages frontend")
        print("🌐 GitHub Pages: https://saurabh-jain-31.github.io/Pixel-Truth-GDG/")
        print("🔗 API calls will be redirected to Render automatically")
    else:
        print("\n⚠️ Render service needs attention")
        print("📋 Next steps:")
        print("1. Check Render dashboard for service status")
        print("2. Look at service logs for errors")
        print("3. Redeploy if necessary")