// Force API configuration override for GitHub Pages deployment
(function() {
    'use strict';
    
    const RENDER_API_URL = 'https://pixel-truth.onrender.com';
    
    console.log('🔧 Loading AGGRESSIVE API redirect...');
    
    // Override all possible API configurations
    window.API_CONFIG = { API_URL: RENDER_API_URL, DEMO_MODE: false };
    window.VITE_API_URL = RENDER_API_URL;
    window.VITE_DEMO_MODE = false;
    
    // Create a global API base URL
    window.API_BASE_URL = RENDER_API_URL;
    
    // Override import.meta.env
    if (typeof window.import !== 'undefined') {
        window.import.meta = window.import.meta || {};
        window.import.meta.env = window.import.meta.env || {};
        window.import.meta.env.VITE_API_URL = RENDER_API_URL;
        window.import.meta.env.VITE_DEMO_MODE = false;
    }
    
    // Function to fix API URLs
    function fixApiUrl(url) {
        if (typeof url !== 'string') return url;
        
        // If it's a relative API path, make it absolute to Render
        if (url.startsWith('/api')) {
            const newUrl = RENDER_API_URL + url;
            console.log('🔄 Fixed relative API URL:', url, '→', newUrl);
            return newUrl;
        }
        
        // If it contains github.io and /api, redirect to Render
        if (url.includes('github.io') && url.includes('/api')) {
            const newUrl = url.replace(/https:\/\/[^\/]+\.github\.io[^\/]*\/api/, RENDER_API_URL + '/api');
            console.log('🔄 Fixed GitHub Pages API URL:', url, '→', newUrl);
            return newUrl;
        }
        
        // If it's trying to call localhost API, redirect to Render
        if (url.includes('localhost') && url.includes('/api')) {
            const newUrl = url.replace(/https?:\/\/localhost:\d+\/api/, RENDER_API_URL + '/api');
            console.log('🔄 Fixed localhost API URL:', url, '→', newUrl);
            return newUrl;
        }
        
        return url;
    }
    
    // Intercept fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        const fixedUrl = fixApiUrl(url);
        
        // Add CORS headers for cross-origin requests
        if (fixedUrl !== url) {
            options.mode = options.mode || 'cors';
            options.credentials = options.credentials || 'omit';
            options.headers = options.headers || {};
            if (typeof options.headers === 'object' && !Array.isArray(options.headers)) {
                options.headers['Content-Type'] = options.headers['Content-Type'] || 'application/json';
            }
        }
        
        return originalFetch.call(this, fixedUrl, options);
    };
    
    // Intercept XMLHttpRequest
    const originalXHROpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, ...args) {
        const fixedUrl = fixApiUrl(url);
        return originalXHROpen.call(this, method, fixedUrl, ...args);
    };
    
    // Intercept axios if it exists (when it loads)
    function interceptAxios() {
        if (window.axios) {
            console.log('🔧 Intercepting Axios requests...');
            
            // Add request interceptor
            window.axios.interceptors.request.use(function (config) {
                if (config.url) {
                    const originalUrl = config.url;
                    config.url = fixApiUrl(config.url);
                    if (config.url !== originalUrl) {
                        console.log('🔄 Axios URL fixed:', originalUrl, '→', config.url);
                    }
                }
                
                // Ensure proper headers for CORS
                config.headers = config.headers || {};
                config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json';
                
                return config;
            }, function (error) {
                return Promise.reject(error);
            });
            
            // Set default base URL
            window.axios.defaults.baseURL = RENDER_API_URL;
            console.log('✅ Axios baseURL set to:', RENDER_API_URL);
        }
    }
    
    // Try to intercept axios immediately and also after a delay
    interceptAxios();
    setTimeout(interceptAxios, 1000);
    setTimeout(interceptAxios, 3000);
    
    // Also try when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', interceptAxios);
    }
    
    console.log('✅ AGGRESSIVE API redirect loaded');
    console.log('🎯 All API calls will be redirected to:', RENDER_API_URL);
    
    // Test the redirect immediately
    setTimeout(() => {
        console.log('🧪 Testing API redirect...');
        fetch('/api/health')
            .then(response => {
                console.log('✅ API redirect test successful:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('✅ API response:', data);
            })
            .catch(error => {
                console.log('❌ API redirect test failed:', error);
            });
    }, 2000);
    
})();