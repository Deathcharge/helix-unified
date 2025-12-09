/**
 * 🌐 Axios Configuration
 * Configured axios instance with interceptors for auth and error handling
 */

import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token to requests
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Get token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('helix_token') : null;
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Log request in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }

    return config;
  },
  (error: AxiosError) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
api.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log response in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
    }

    return response;
  },
  (error: AxiosError) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data as any;

      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          if (typeof window !== 'undefined') {
            localStorage.removeItem('helix_token');
            localStorage.removeItem('helix_user');
            
            // Only redirect if not already on auth page
            if (!window.location.pathname.startsWith('/auth')) {
              window.location.href = '/auth/login?expired=true';
            }
          }
          break;

        case 403:
          // Forbidden - show upgrade prompt
          console.error('[API] Forbidden:', data?.message || 'Access denied');
          break;

        case 404:
          // Not found
          console.error('[API] Not found:', error.config?.url);
          break;

        case 429:
          // Rate limit exceeded
          const retryAfter = error.response.headers['retry-after'];
          console.error(`[API] Rate limit exceeded. Retry after ${retryAfter} seconds`);
          break;

        case 500:
        case 502:
        case 503:
        case 504:
          // Server errors
          console.error('[API] Server error:', status, data?.message);
          break;

        default:
          console.error('[API] Error:', status, data?.message || error.message);
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('[API] No response received:', error.message);
      
      // Check if it's a network error
      if (error.message === 'Network Error') {
        console.error('[API] Network error - check your internet connection');
      }
    } else {
      // Error setting up request
      console.error('[API] Request setup error:', error.message);
    }

    return Promise.reject(error);
  }
);

// Helper functions for common API calls
export const apiHelpers = {
  /**
   * Get current user info
   */
  async getCurrentUser() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  /**
   * Login with email/password
   */
  async login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password });
    
    // Store token and user info
    if (typeof window !== 'undefined' && response.data) {
      localStorage.setItem('helix_token', response.data.access_token);
      localStorage.setItem('helix_user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  /**
   * Signup with email/password
   */
  async signup(email: string, password: string, name: string) {
    const response = await api.post('/auth/signup', { email, password, name });
    
    // Store token and user info
    if (typeof window !== 'undefined' && response.data) {
      localStorage.setItem('helix_token', response.data.access_token);
      localStorage.setItem('helix_user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  /**
   * Logout
   */
  async logout() {
    try {
      await api.post('/auth/logout');
    } finally {
      // Clear local storage regardless of API response
      if (typeof window !== 'undefined') {
        localStorage.removeItem('helix_token');
        localStorage.removeItem('helix_user');
        window.location.href = '/';
      }
    }
  },

  /**
   * Get demo login token
   */
  async demoLogin() {
    const response = await api.post('/auth/demo-login');
    
    // Store token and user info
    if (typeof window !== 'undefined' && response.data) {
      localStorage.setItem('helix_token', response.data.access_token);
      localStorage.setItem('helix_user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },
};

export default api;
