#!/usr/bin/env python3
"""
Test to diagnose blank page issues
"""
import os
import requests

def test_file_accessibility():
    """Test if files are accessible"""
    print("🔍 Testing File Accessibility")
    print("=" * 40)
    
    files_to_check = [
        'direct-scan.html',
        'simple-scan.html',
        'index.html',
        'api-config.js',
        'fix-api-config.js',
        'emergency-mock-api.js'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({size:,} bytes)")
            
            # Check if it's HTML and has basic structure
            if file_path.endswith('.html'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '<html' in content and '<body' in content:
                        print(f"      ✅ Valid HTML structure")
                    else:
                        print(f"      ❌ Invalid HTML structure")
                    
                    if 'script' in content:
                        print(f"      ✅ Contains JavaScript")
                    else:
                        print(f"      ⚠️ No JavaScript found")
        else:
            print(f"   ❌ {file_path} - Not found")

def test_github_pages_status():
    """Test GitHub Pages status"""
    print("\n🌐 Testing GitHub Pages Status")
    print("=" * 40)
    
    urls_to_test = [
        "https://saurabh-jain-31.github.io/Pixel-Truth/",
        "https://saurabh-jain-31.github.io/Pixel-Truth/direct-scan.html",
        "https://saurabh-jain-31.github.io/Pixel-Truth/simple-scan.html",
        "https://saurabh-jain-31.github.io/Pixel-Truth/index.html"
    ]
    
    for url in urls_to_test:
        try:
            response = requests.get(url, timeout=10)
            print(f"   {url}")
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"      Content-Type: {content_type}")
                
                if 'text/html' in content_type:
                    content = response.text
                    if len(content) < 100:
                        print(f"      ⚠️ Very short content ({len(content)} chars)")
                    elif '<html' in content:
                        print(f"      ✅ Valid HTML content ({len(content)} chars)")
                    else:
                        print(f"      ❌ Invalid HTML content")
                else:
                    print(f"      ❌ Not HTML content")
                    
            elif response.status_code == 404:
                print(f"      ❌ File not found (GitHub Pages may not be enabled)")
            else:
                print(f"      ⚠️ Unexpected status code")
                
        except requests.exceptions.ConnectionError:
            print(f"   {url}")
            print(f"      ❌ Connection failed (GitHub Pages not accessible)")
        except Exception as e:
            print(f"   {url}")
            print(f"      ❌ Error: {e}")

def create_minimal_test_page():
    """Create a minimal test page"""
    print("\n🛠️ Creating Minimal Test Page")
    print("=" * 40)
    
    minimal_html = """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>✅ Test Page Working</h1>
    <p>If you can see this, the basic HTML is working.</p>
    <button onclick="testJS()">Test JavaScript</button>
    <div id="result"></div>
    
    <script>
        console.log('✅ JavaScript is working');
        
        function testJS() {
            document.getElementById('result').innerHTML = '✅ JavaScript click event working';
            console.log('✅ Button clicked');
        }
        
        // Test basic functionality
        document.addEventListener('DOMContentLoaded', function() {
            console.log('✅ DOM loaded');
            document.getElementById('result').innerHTML = '✅ DOM ready';
        });
    </script>
</body>
</html>"""
    
    with open('test-page.html', 'w', encoding='utf-8') as f:
        f.write(minimal_html)
    
    print("   ✅ Created test-page.html")
    print("   📝 You can test this locally by opening test-page.html in browser")

def diagnose_blank_page():
    """Provide diagnosis for blank page issues"""
    print("\n🔍 Blank Page Diagnosis")
    print("=" * 40)
    
    print("Common causes of blank pages:")
    print("1. ❌ JavaScript errors preventing page load")
    print("2. ❌ Missing or broken CSS/JS file references")
    print("3. ❌ CORS issues with external scripts")
    print("4. ❌ GitHub Pages not enabled")
    print("5. ❌ File encoding issues")
    print("6. ❌ Browser caching old version")
    
    print("\nSolutions to try:")
    print("1. ✅ Open browser developer tools (F12)")
    print("2. ✅ Check Console tab for JavaScript errors")
    print("3. ✅ Check Network tab for failed requests")
    print("4. ✅ Try hard refresh (Ctrl+F5)")
    print("5. ✅ Test simple-scan.html (simpler version)")
    print("6. ✅ Enable GitHub Pages in repository settings")

if __name__ == "__main__":
    print("🧪 Blank Page Diagnostic Tool")
    print("=" * 50)
    
    test_file_accessibility()
    test_github_pages_status()
    create_minimal_test_page()
    diagnose_blank_page()
    
    print("\n🎯 Next Steps:")
    print("1. Enable GitHub Pages if not done")
    print("2. Try simple-scan.html for basic functionality")
    print("3. Check browser console for errors")
    print("4. Test with test-page.html first")