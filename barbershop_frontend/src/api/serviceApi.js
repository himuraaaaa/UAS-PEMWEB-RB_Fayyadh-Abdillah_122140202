// src/api/serviceApi.js
import api from './index';

export const getServices = () => api.get('/api/services');
export const getService = (id) => api.get(`/api/service/${id}`);
export const createService = (serviceData) => api.post('/api/service/create', serviceData);
export const updateService = (id, serviceData) => api.put(`/api/service/update/${id}`, serviceData);
export const deleteService = (id) => api.delete(`/api/service/delete/${id}`);
