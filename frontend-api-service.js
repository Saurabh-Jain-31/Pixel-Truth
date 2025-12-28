// Frontend API Service - Place in frontend/src/services/api.js

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '' // Same domain in production
  : 'http://localhost:8000'; // Backend dev server

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('token');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  removeToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  async apiCall(endpoint, options = {}) {
    const url = `${this.baseURL}/api${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (this.token) {
      config.headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  // Auth methods
  async register(userData) {
    return this.apiCall('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials) {
    const response = await this.apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    if (response.access_token) {
      this.setToken(response.access_token);
    }
    
    return response;
  }

  // Analysis methods
  async analyzeImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    return this.apiCall('/analyze/image', {
      method: 'POST',
      headers: {
        // Remove Content-Type to let browser set it with boundary
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });
  }

  async analyzePDF(file) {
    const formData = new FormData();
    formData.append('file', file);

    return this.apiCall('/analyze/pdf', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });
  }

  // History methods
  async getHistory(page = 1, pageSize = 20) {
    return this.apiCall(`/history?page=${page}&page_size=${pageSize}`);
  }
}

export default new ApiService();