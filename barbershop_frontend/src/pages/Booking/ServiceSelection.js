// src/pages/Booking/ServiceSelection.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { getServices } from '../../api/serviceApi';
import './BookingPages.css';

const ServiceSelection = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedService, setSelectedService] = useState(null);
  const auth = useAuth();
  console.log('useAuth() result:', auth);
  const bookingData = auth?.bookingData || {};
  const updateBookingData = auth?.updateBookingData || (() => {});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await getServices();
        setServices(response.data?.data || []);
        // If there's already a selected service in the context, select it
        if (bookingData.service) {
          setSelectedService(bookingData.service);
        }
      } catch (error) {
        console.error('Error fetching services:', error);
        setServices([]);
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, [bookingData.service]);

  const handleServiceSelect = (service) => {
    setSelectedService(service);
  };

  const handleContinue = () => {
    if (selectedService) {
      updateBookingData({ service: selectedService });
      navigate('/booking/barbers');
    } else {
      alert('Please select a service to continue.');
    }
  };

  if (loading) {
    return (
      <div className="booking-page">
        <div className="container">
          <h2>Loading services...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="booking-page">
      <div className="container">
        <div className="booking-header">
          <h2>Select a Service</h2>
          <p>Choose from our premium services</p>
        </div>
        
        <div className="booking-progress">
          <div className="progress-step active">1. Select Service</div>
          <div className="progress-step">2. Choose Barber</div>
          <div className="progress-step">3. Book Appointment</div>
        </div>
        
        <div className="services-grid">
          {services.map(service => (
            <div 
              key={service.id} 
              className={`service-card ${selectedService && selectedService.id === service.id ? 'selected' : ''}`}
              onClick={() => handleServiceSelect(service)}
            >
              <h2>{service.name || service.title}</h2>
              <p>{service.description}</p>
              <div className="service-price">${service.price}</div>
              {selectedService && selectedService.id === service.id && (
                <div className="selected-badge">
                  <i className="fas fa-check"></i>
                </div>
              )}
            </div>
          ))}
        </div>
        
        <div className="booking-actions">
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/')}
          >
            Back to Home
          </button>
          <button 
            className="btn btn-primary"
            onClick={handleContinue}
            disabled={!selectedService}
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  );
};

export default ServiceSelection;