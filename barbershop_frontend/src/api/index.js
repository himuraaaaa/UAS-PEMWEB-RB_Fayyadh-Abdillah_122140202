import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:6543',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Add request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    console.log('Request interceptor - Token:', token);
    console.log('Request interceptor - URL:', config.url);
    console.log('Request interceptor - Method:', config.method);
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Request interceptor - Headers:', config.headers);
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('Response interceptor - Status:', response.status);
    console.log('Response interceptor - Data:', response.data);
    return response;
  },
  (error) => {
    console.error('Response interceptor error:', error);
    console.error('Response interceptor - Status:', error.response?.status);
    console.error('Response interceptor - Data:', error.response?.data);
    
    if (error.response?.status === 401) {
      console.log('Unauthorized access detected, redirecting to login...');
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const login = async (credentials) => {
  try {
    console.log('Login attempt with credentials:', credentials);
    const response = await api.post('/api/auth/login', credentials);
    console.log('Login response:', response.data);
    
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      console.log('Token stored in localStorage');
    } else {
      console.warn('No token received in login response');
    }
    return response;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const register = async (userData) => {
  try {
    console.log('Registration attempt with data:', userData);
    const response = await api.post('/api/auth/register', userData);
    console.log('Registration response:', response.data);
    return response;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// Barber APIs
export const getBarbers = () => api.get('/api/barbers');
export const getBarber = (id) => api.get(`/api/barber/${id}`);
export const createBarber = (barberData) => api.post('/api/barber/create', barberData);
export const updateBarber = (id, barberData) => api.put(`/api/barber/update/${id}`, barberData);
export const deleteBarber = (id) => api.delete(`/api/barber/delete/${id}`);

// Service APIs
export const getServices = () => api.get('/api/services');
export const getService = (id) => api.get(`/api/service/${id}`);
export const createService = (serviceData) => api.post('/api/service/create', serviceData);
export const updateService = (id, serviceData) => api.put(`/api/service/update/${id}`, serviceData);
export const deleteService = (id) => api.delete(`/api/service/delete/${id}`);

// Appointment APIs
export const getAppointments = () => api.get('/api/appointments');
export const getAppointment = (id) => api.get(`/api/appointment/${id}`);
export const createAppointment = (appointmentData) => api.post('/api/appointment/create', appointmentData);
export const updateAppointment = (id, appointmentData) => api.put(`/api/appointment/update/${id}`, appointmentData);
export const updateAppointmentStatus = (id, statusData) => api.put(`/api/appointment/update-status/${id}`, statusData);
export const deleteAppointment = (id) => api.delete(`/api/appointment/delete/${id}`);

export default api; 