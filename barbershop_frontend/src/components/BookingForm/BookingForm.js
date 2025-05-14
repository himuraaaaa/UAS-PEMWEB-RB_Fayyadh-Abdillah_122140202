import React, { useState, useEffect } from 'react';
import { submitBooking } from '../../api/bookingApi';
import Button from '../Button/Button';
import './BookingForm.css';

const BookingForm = () => {
  const [bookingData, setBookingData] = useState({
    service: '',
    barber: '',
    date: '',
    time: '',
    name: '',
    email: '',
    phone: ''
  });
  const [loading, setLoading] = useState(false);
  const [services, setServices] = useState([
    'Classic Haircut',
    'Beard Trim',
    'Hot Towel Shave',
    'Hair Coloring',
    'Kids Haircut',
    'Hair Treatment'
  ]);

  const barbers = [
    'John Doe',
    'Mike Smith',
    'David Wilson',
    'Robert Johnson'
  ];

  const timeSlots = [
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBookingData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await submitBooking(bookingData);
      if (response.success) {
        alert('Thank you for booking with us! We will confirm your appointment shortly.');
        setBookingData({
          service: '',
          barber: '',
          date: '',
          time: '',
          name: '',
          email: '',
          phone: ''
        });
      }
    } catch (error) {
      alert('Something went wrong. Please try again later.');
      console.error('Booking error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="booking-form-container">
      <h3>Book Your Appointment</h3>
      <form className="booking-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Select Service</label>
          <select 
            name="service" 
            value={bookingData.service}
            onChange={handleChange}
            required
          >
            <option value="">Choose a service</option>
            {services.map((service, index) => (
              <option key={index} value={service}>{service}</option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label>Select Barber</label>
          <select 
            name="barber" 
            value={bookingData.barber}
            onChange={handleChange}
            required
          >
            <option value="">Choose a barber</option>
            {barbers.map((barber, index) => (
              <option key={index} value={barber}>{barber}</option>
            ))}
          </select>
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label>Select Date</label>
            <input 
              type="date" 
              name="date" 
              value={bookingData.date}
              onChange={handleChange}
              required 
            />
          </div>
          
          <div className="form-group">
            <label>Select Time</label>
            <select 
              name="time" 
              value={bookingData.time}
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
          <label>Your Name</label>
          <input 
            type="text" 
            name="name" 
            placeholder="Enter your name" 
            value={bookingData.name}
            onChange={handleChange}
            required 
          />
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label>Your Email</label>
            <input 
              type="email" 
              name="email" 
              placeholder="Enter your email" 
              value={bookingData.email}
              onChange={handleChange}
              required 
            />
          </div>
          
          <div className="form-group">
            <label>Your Phone</label>
            <input 
              type="tel" 
              name="phone" 
              placeholder="Enter your phone number" 
              value={bookingData.phone}
              onChange={handleChange}
              required 
            />
          </div>
        </div>
        
        <Button 
          type="primary" 
          className="booking-btn" 
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Book Appointment'}
        </Button>
      </form>
    </div>
  );
};

export default BookingForm;