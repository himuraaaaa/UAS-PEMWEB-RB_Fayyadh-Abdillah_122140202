// src/pages/Booking/BookingSection.js
import { useAuth } from '../../contexts/AuthContext';
import Button from '../../components/Button/Button';
import React from 'react';
import { Link } from 'react-router-dom';

const BookingSection = () => {
  const { isAuthenticated } = useAuth();

  return (
    <section id="booking" className="booking-section">
      <div className="container">
        <div className="section-header">
          <h2>Book an Appointment</h2>
          <p>Schedule your visit and experience our premium services</p>
        </div>
        
        <div className="booking-container">
          <div className="booking-image">
            <img src="/assets/images/booking-image.jpg" alt="Booking" />
            <div className="booking-overlay">
              <h3>Why Book With Us?</h3>
              <ul>
                <li>Professional barbers with years of experience</li>
                <li>Premium products for the best results</li>
                <li>Comfortable and relaxing atmosphere</li>
                <li>Convenient online booking system</li>
                <li>Flexible scheduling options</li>
              </ul>
            </div>
          </div>
          
          <div className="booking-form-container">
            <h3>Ready to Book Your Appointment?</h3>
            <p>Follow our simple 3-step booking process:</p>
            
            <div className="booking-steps">
              <div className="booking-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>Choose Your Service</h4>
                  <p>Select from our range of premium haircuts and grooming services.</p>
                </div>
              </div>
              
              <div className="booking-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>Select Your Barber</h4>
                  <p>Pick your preferred hair artist based on their expertise and style.</p>
                </div>
              </div>
              
              <div className="booking-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>Book Your Time</h4>
                  <p>Choose a convenient date and time for your appointment.</p>
                </div>
              </div>
            </div>
            
            <div className="booking-cta">
              {isAuthenticated ? (
                <Link to="/booking/services">
                  <Button type="primary" className="booking-btn">Start Booking Now</Button>
                </Link>
              ) : (
                <Link to="/login?redirect=/booking/services">
                  <Button type="primary" className="booking-btn">Login to Book</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default BookingSection;