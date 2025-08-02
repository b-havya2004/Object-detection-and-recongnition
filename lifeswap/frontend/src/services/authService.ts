import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add request interceptor to include auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email); // FastAPI OAuth2PasswordRequestForm expects 'username'
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData);
    const { access_token } = response.data;
    
    // Get user data after login
    const userResponse = await api.get('/users/me', {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    
    return {
      token: access_token,
      user: userResponse.data
    };
  },

  register: async (userData: {
    email: string;
    username: string;
    password: string;
    full_name?: string;
    country?: string;
    age_group?: string;
    interests?: string[];
  }) => {
    const response = await api.post('/auth/register', userData);
    const user = response.data;
    
    // Auto-login after registration
    const loginResult = await authService.login(userData.email, userData.password);
    return loginResult;
  },

  getCurrentUser: async (token: string) => {
    const response = await api.get('/users/me', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },

  logout: async () => {
    await api.post('/auth/logout');
  },

  verifyToken: async (token: string) => {
    const response = await api.get('/auth/verify', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
};

export default api;