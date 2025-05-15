import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from '../pages/Home/Home';
import Login from '../pages/Login/Login';
import Register from '../pages/Register/Register';
import ServiceSelection from '../pages/Booking/ServiceSelection';
import BarberSelection from '../pages/Booking/BarberSelection';
import BookingForm from '../pages/Booking/BookingForm';
import BookingConfirmation from '../pages/Booking/BookingConfirmation';
import Navbar from '../components/Navbar/Navbar';
import Footer from '../components/Footer/Footer';
import RequireAuth from './RequireAuth';

const AppRoutes = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected booking routes */}
        <Route element={<RequireAuth />}>
          <Route path="/booking/services" element={<ServiceSelection />} />
          <Route path="/booking/barbers" element={<BarberSelection />} />
          <Route path="/booking/form" element={<BookingForm />} />
          <Route path="/booking/confirmation" element={<BookingConfirmation />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default AppRoutes;
