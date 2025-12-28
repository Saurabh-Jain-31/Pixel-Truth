import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { isDemoMode, demoAPI, initDemoData } from '../utils/demoMode';

const AuthContext = createContext();

// API Base URL configuration for Python FastAPI backend
const getApiBaseUrl = () => {
  // Production environment
  if (import.meta.env.PROD) {
    return import.meta.env.VITE_API_URL || 'https://pixel-truth-backend.onrender.com';
  }
  
  // Development environment - Python FastAPI runs on port 5000
  return import.meta.env.VITE_API_URL || 'http://localhost:5000';
};

// Configure axios defaults - Remove baseURL to use Vite proxy
const API_BASE_URL = getApiBaseUrl();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isDemo, setIsDemo] = useState(isDemoMode());

  // Initialize demo data if in demo mode
  useEffect(() => {
    if (isDemo) {
      initDemoData();
    }
  }, [isDemo]);

  // Set up axios defaults
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      if (isDemo) {
        // Demo mode - check for demo user
        const demoUser = localStorage.getItem('demoUser');
        if (demoUser) {
          setUser(JSON.parse(demoUser));
        }
        setLoading(false);
        return;
      }

      if (token) {
        try {
          const response = await axios.get('/api/auth/me');
          setUser(response.data.user);
        } catch (error) {
          console.error('Auth check failed:', error);
          // If backend is not available, enable demo mode
          console.log('🔄 Backend not available, enabling demo mode');
          setIsDemo(true);
          initDemoData();
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token, isDemo]);

  const login = async (email, password) => {
    try {
      if (isDemo) {
        const result = await demoAPI.login(email, password);
        localStorage.setItem('demoUser', JSON.stringify(result.user));
        setUser(result.user);
        return { success: true };
      }

      const response = await axios.post('/api/auth/login', { email, password });
      const { token: newToken, user: userData } = response.data;
      
      localStorage.setItem('token', newToken);
      setToken(newToken);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Login failed'
      };
    }
  };

  const register = async (username, email, password) => {
    try {
      console.log('🔍 Attempting to register:', { username, email });
      console.log('🌐 Demo mode:', isDemo);
      
      if (isDemo) {
        const result = await demoAPI.register({ username, email, password });
        localStorage.setItem('demoUser', JSON.stringify(result.user));
        setUser(result.user);
        return { success: true };
      }

      console.log('🌐 API Base URL:', API_BASE_URL);
      
      const response = await axios.post('/api/auth/register', {
        username,
        email,
        password
      });
      
      console.log('✅ Registration successful:', response.data);
      
      const { token: newToken, user: userData } = response.data;
      
      localStorage.setItem('token', newToken);
      setToken(newToken);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error('❌ Registration error:', error);
      console.error('❌ Error response:', error.response?.data);
      
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Registration failed'
      };
    }
  };

  const logout = async () => {
    try {
      if (!isDemo) {
        await axios.post('/api/auth/logout');
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('demoUser');
      setToken(null);
      setUser(null);
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const updateUser = (userData) => {
    setUser(prev => ({ ...prev, ...userData }));
  };

  const testConnection = async () => {
    try {
      console.log('🧪 Testing backend connection...');
      const response = await axios.get('/api/auth/test');
      console.log('✅ Backend connection test successful:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Backend connection test failed:', error);
      throw error;
    }
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    updateUser,
    testConnection,
    isAuthenticated: !!user,
    isDemo
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};