import React, { useState, useEffect } from 'react';
import ServiceCard from '../components/ServiceCard/ServiceCard';  // satu tingkat naik dari api ke src
import { getServices } from './serviceApi'; // karena serviceApi.js di folder yang sama dengan bookingApi.js

// src/api/bookingApi.js
export const submitBooking = async (bookingData) => {
  // Simulasi API call
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Booking submitted:', bookingData);
      resolve({ success: true, message: 'Booking successful' });
    }, 1000);
  });
};

// src/api/authApi.js
export const login = async (credentials) => {
  // Simulasi API call
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Login attempt:', credentials);
      resolve({ success: true, token: 'sample-token', user: { name: 'John Doe' } });
    }, 1000);
  });
};

// src/api/serviceApi.js
const ServicesSection = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const data = await getServices();
        setServices(data);
      } catch (error) {
        console.error('Error fetching services:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, []);

  if (loading) {
    return (
      <section id="services" className="services-section">
        <div className="container">
          <div className="section-header">
            <h2>Our Services</h2>
            <p>Loading our premium services...</p>
          </div>
          <div className="loading-spinner"></div>
        </div>
      </section>
    );
  }

  return (
    <section id="services" className="services-section">
      <div className="container">
        <div className="section-header">
          <h2>Our Services</h2>
          <p>Professional haircuts and grooming services for the modern gentleman</p>
        </div>
        <div className="services-grid">
          {services.map(service => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;
