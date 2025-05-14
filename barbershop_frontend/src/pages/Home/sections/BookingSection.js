import React from 'react';
import BookingForm from '../../../components/BookingForm/BookingForm';

const BookingSection = () => {
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
          
          <BookingForm />
        </div>
      </div>
    </section>
  );
};

export default BookingSection;