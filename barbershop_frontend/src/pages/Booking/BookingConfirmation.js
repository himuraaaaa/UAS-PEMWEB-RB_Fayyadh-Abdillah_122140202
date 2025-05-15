import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { QRCodeCanvas } from 'qrcode.react';
import './BookingPages.css';

const BookingConfirmation = () => {
  const { bookingData, currentUser } = useAuth();
  const navigate = useNavigate();

  if (!bookingData.service || !bookingData.barber || !bookingData.date || !bookingData.time) {
    // Jika data booking belum lengkap, redirect ke halaman awal booking
    navigate('/booking/services');
    return null;
  }

  // Dummy payment URL (bisa diganti sesuai kebutuhan)
  const paymentUrl = `https://payment.example.com/pay?user=${currentUser?.email || ''}&service=${bookingData.service?.id}&date=${bookingData.date}&time=${bookingData.time}`;

  return (
    <div className="booking-page">
      <div className="container booking-confirmation">
        <h2>Booking Confirmation</h2>
        <p>Thank you for your booking, {bookingData.name || currentUser?.name}!</p>

        <div className="confirmation-details">
          <h3>Booking Details</h3>
          <ul>
            <li><strong>Service:</strong> {bookingData.service.title} ({bookingData.service.price})</li>
            <li><strong>Barber:</strong> {bookingData.barber.name} - {bookingData.barber.position}</li>
            <li><strong>Date:</strong> {bookingData.date}</li>
            <li><strong>Time:</strong> {bookingData.time}</li>
            <li><strong>Name:</strong> {bookingData.name}</li>
            <li><strong>Email:</strong> {bookingData.email}</li>
            <li><strong>Phone:</strong> {bookingData.phone}</li>
            {bookingData.notes && <li><strong>Notes:</strong> {bookingData.notes}</li>}
          </ul>
        </div>

        <div className="payment-section">
          <h3>Payment</h3>
          <p>Please scan the QR code below to complete your payment:</p>
          <div className="qr-code">
            <QRCodeCanvas value={paymentUrl} size={200} />
          </div>
          <p className="payment-instruction">Scan this QR code with your payment app to proceed.</p>
        </div>

        <button className="btn btn-primary" onClick={() => navigate('/')}>
          Back to Home
        </button>
      </div>
    </div>
  );
};

export default BookingConfirmation;
