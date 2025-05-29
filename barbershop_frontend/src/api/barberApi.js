import api from './index';

export const getBarbers = () => api.get('/api/barbers');
export const getBarber = (id) => api.get(`/api/barber/${id}`);
export const createBarber = (barberData) => api.post('/api/barber/create', barberData);
export const updateBarber = (id, barberData) => api.put(`/api/barber/update/${id}`, barberData);
export const deleteBarber = (id) => api.delete(`/api/barber/delete/${id}`);