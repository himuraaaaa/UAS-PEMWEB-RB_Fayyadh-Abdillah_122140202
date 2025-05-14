// src/pages/Booking/BookingForm.js (lanjutan)
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { submitBooking } from '../../api/bookingApi';
import './BookingPages.css';

const BookingForm = () => {
  const { bookingData, updateBookingData, currentUser } = useAuth();
  const [formData, setFormData] = useState({
    date: bookingData.date || '',
    time: bookingData.time || '',
    name: bookingData.name || currentUser?.name || '',
    email: bookingData.email || currentUser?.email || '',
    phone: bookingData.phone || currentUser?.phone || '',
    notes: bookingData.notes || ''
  });
  const [loading, setLoading] = useState(false);
  const [timeSlots, setTimeSlots] = useState([]);
  const navigate = useNavigate();

  // Check if service and barber are selected
  useEffect(() => {
    if (!bookingData.service) {
      navigate('/booking/services');
    } else if (!bookingData.barber) {
      navigate('/booking/barbers');
    }
  }, [bookingData.service, bookingData.barber, navigate]);

  // Generate available time slots
  useEffect(() => {
    const slots = [
      '09:00 AM',
      '10:00 AM',
      '11:00 AM',
      '12:00 PM',
      '01:00 PM',
      '02:00 PM',
      '03:00 PM',
      '04:00 PM',
      '05:00 PM',
      '06:00 PM',
      '07:00 PM'
    ];
    setTimeSlots(slots);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.date || !formData.time) {
      alert('Please select a date and time for your appointment.');
      return;
    }
    
    setLoading(true);
    
    try {
      // Update booking data in context
      const completeBookingData = {
        ...bookingData,
        ...formData
      };
      updateBookingData(formData);
      
      // Submit booking to API
      const response = await submitBooking(completeBookingData);
      
      if (response.success) {
        alert('Your appointment has been booked successfully! We will send you a confirmation email shortly.');
        navigate('/');
      } else {
        alert('There was an issue with your booking. Please try again.');
      }
    } catch (error) {
      console.error('Booking error:', error);
      alert('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    // Save current form data to context before navigating back
    updateBookingData(formData);
    navigate('/booking/barbers');
  };

  // Get today's date in YYYY-MM-DD format for min date attribute
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="booking-page">
      <div className="container">
        <div className="booking-header">
          <h2>Book Your Appointment</h2>
          <p>Complete your booking details</p>
        </div>
        
        <div className="booking-progress">
          <div className="progress-step completed">1. Select Service</div>
          <div className="progress-step completed">2. Choose Barber</div>
          <div className="progress-step active">3. Book Appointment</div>
        </div>
        
        <div className="booking-summary">
          <h3>Booking Summary</h3>
          <div className="summary-details">
            <div className="summary-item">
              <span className="summary-label">Service:</span>
              <span className="summary-value">{bookingData.service?.title}</span>
              <span className="summary-price">{bookingData.service?.price}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Barber:</span>
              <span className="summary-value">{bookingData.barber?.name}</span>
              <span className="summary-position">{bookingData.barber?.position}</span>
            </div>
          </div>
        </div>
        
        <form className="booking-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="date">Select Date</label>
              <input 
                type="date" 
                id="date"
                name="date" 
                value={formData.date}
                onChange={handleChange}
                min={today}
                required 
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="time">Select Time</label>
              <select 
                id="time"
                name="time" 
                value={formData.time}
                onChange={handleChange}
                required
              >
                <option value="">Choose a time</option>
                {timeSlots.map((time, index) => (
                  <option key={index} value={time}>{time}</option>
                ))}
              </select>
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="name">Your Name</label>
            <input 
              type="text" 
              id="name"
              name="name" 
              placeholder="Enter your full name" 
              value={formData.name}
              onChange={handleChange}
              required 
            />
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input 
                type="email" 
                id="email"
                name="email" 
                placeholder="Enter your email" 
                value={formData.email}
                onChange={handleChange}
                required 
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input 
                type="tel" 
                id="phone"
                name="phone" 
                placeholder="Enter your phone number" 
                value={formData.phone}
                onChange={handleChange}
                required 
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="notes">Additional Notes (Optional)</label>
            <textarea 
              id="notes"
              name="notes" 
              placeholder="Any special requests or information we should know?" 
              value={formData.notes}
              onChange={handleChange}
              rows="3"
            ></textarea>
          </div>
          
          <div className="booking-actions">
            <button 
              type="button"
              className="btn btn-secondary"
              onClick={handleBack}
            >
              Back
            </button>
            <button 
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Confirm Booking'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BookingForm;
