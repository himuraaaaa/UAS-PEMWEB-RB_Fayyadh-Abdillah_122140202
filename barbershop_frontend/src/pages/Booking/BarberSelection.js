// src/pages/Booking/BarberSelection.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../api';
import './BookingPages.css';

const BACKEND_URL = "http://localhost:6543";

const BarberSelection = () => {
  const [barbers, setBarbers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBarber, setSelectedBarber] = useState(null);
  const auth = useAuth();
  console.log('useAuth() result:', auth);
  const bookingData = auth?.bookingData || {};
  const updateBookingData = auth?.updateBookingData || (() => {});
  const navigate = useNavigate();

  // Check if service is selected
  useEffect(() => {
    if (!bookingData.service) {
      navigate('/booking/services');
    }
  }, [bookingData.service, navigate]);

  // Fetch barbers (simulated)
  useEffect(() => {
    const fetchBarbers = async () => {
      try {
        const response = await api.get('/api/barbers');
        setBarbers(response.data?.data || []);
        if (bookingData.barber) {
          setSelectedBarber(bookingData.barber);
        }
      } catch (error) {
        console.error('Error fetching barbers:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBarbers();
  }, [bookingData.barber]);

  const handleBarberSelect = (barber) => {
    setSelectedBarber(barber);
  };

  const handleContinue = () => {
    if (selectedBarber) {
      updateBookingData({ barber: selectedBarber });
      navigate('/booking/form');
    } else {
      alert('Please select a barber to continue.');
    }
  };

  const handleBack = () => {
    navigate('/booking/services');
  };

  if (loading) {
    return (
      <div className="booking-page">
        <div className="container">
          <h2>Loading barbers...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="booking-page">
      <div className="container">
        <div className="booking-header">
          <h2>Select a Barber</h2>
          <p>Choose your preferred hair artist</p>
        </div>
        
        <div className="booking-progress">
          <div className="progress-step completed">1. Select Service</div>
          <div className="progress-step active">2. Choose Barber</div>
          <div className="progress-step">3. Book Appointment</div>
        </div>
        
        <div className="selected-service-summary">
          <h3>Selected Service:</h3>
          <div className="service-info">
            <span className="service-name">{bookingData.service?.title}</span>
            <span className="service-price">${bookingData.service?.price}</span>
          </div>
        </div>
        
        <div className="barbers-grid">
          {barbers.map(barber => (
            <div 
              key={barber.id} 
              className={`barber-card ${selectedBarber && selectedBarber.id === barber.id ? 'selected' : ''}`}
              onClick={() => handleBarberSelect(barber)}
            >
              <div className="barber-image">
                <img 
                  src={barber.image && !barber.image.startsWith('http') ? `${BACKEND_URL}/assets/barbers/${barber.image}` : barber.image} 
                  alt={barber.name} 
                  style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '8px' }}
                />
                <div className="barber-social">
                  <a href={barber.social.instagram} target="_blank" rel="noopener noreferrer">
                    <i className="fab fa-instagram"></i>
                  </a>
                </div>
              </div>
              <div className="barber-info">
                <h3>{barber.name}</h3>
                <p className="barber-position">{barber.position}</p>
              </div>
              {selectedBarber && selectedBarber.id === barber.id && (
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
            onClick={handleBack}
          >
            Back
          </button>
          <button 
            className="btn btn-primary"
            onClick={handleContinue}
            disabled={!selectedBarber}
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  );
};

export default BarberSelection;
