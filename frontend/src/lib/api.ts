// src/lib/api.ts
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Flask backend
});

instance.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default instance;
