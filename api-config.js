// Dynamic API configuration for GitHub Pages
window.API_CONFIG = {
    API_URL: 'https://pixel-truth.onrender.com',
    DEMO_MODE: false
};

// Override any existing API configuration
window.VITE_API_URL = 'https://pixel-truth.onrender.com';
window.VITE_DEMO_MODE = false;

console.log('🔧 API Configuration loaded:', window.API_CONFIG);
console.log('🔧 Overriding API URL to:', window.VITE_API_URL);