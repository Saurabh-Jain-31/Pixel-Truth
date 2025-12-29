// Immediate Render service wake-up and test
(function() {
    'use strict';
    
    const RENDER_API_URL = 'https://pixel-truth.onrender.com';
    
    console.log('🚀 Starting immediate Render wake-up...');
    
    // Function to wake up Render service
    function wakeUpRender() {
        console.log('⏰ Waking up Render service (this may take 30-60 seconds)...');
        
        // Make multiple requests to wake up the service
        const endpoints = ['/', '/api/health', '/api/auth/test'];
        
        endpoints.forEach((endpoint, index) => {
            setTimeout(() => {
                fetch(RENDER_API_URL + endpoint, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'omit'
                })
                .then(response => {
                    console.log(`✅ Render wake-up ${endpoint}:`, response.status);
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error(`HTTP ${response.status}`);
                })
                .then(data => {
                    console.log(`📄 Render response ${endpoint}:`, data);
                })
                .catch(error => {
                    console.log(`⚠️ Render wake-up ${endpoint} error:`, error.message);
                });
            }, index * 2000); // Stagger requests
        });
    }
    
    // Start wake-up process immediately
    wakeUpRender();
    
    // Test login endpoint specifically
    setTimeout(() => {
        console.log('🧪 Testing login endpoint...');
        
        fetch(RENDER_API_URL + '/api/auth/login', {
            method: 'POST',
            mode: 'cors',
            credentials: 'omit',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: 'test@example.com',
                password: 'test123'
            })
        })
        .then(response => {
            console.log('✅ Login test response:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('✅ Login test data:', data);
        })
        .catch(error => {
            console.log('❌ Login test error:', error);
        });
    }, 10000); // Wait 10 seconds before testing login
    
    console.log('🎯 Render wake-up initiated');
    
})();