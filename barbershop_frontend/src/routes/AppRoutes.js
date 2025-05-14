// src/routes/AppRoutes.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Home from '../pages/Home/Home';
import Login from '../pages/Login/Login';
import Register from '../pages/Register/Register';
import ServiceSelection from '../pages/Booking/ServiceSelection';
import BarberSelection from '../pages/Booking/BarberSelection';
import BookingForm from '../pages/Booking/BookingForm';
import Navbar from '../components/Navbar/Navbar';
import Footer from '../components/Footer/Footer';


// Protected route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();


  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

const AppRoutes = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Booking Flow */}
        <Route 
          path="/booking/services" 
          element={
            <ProtectedRoute>
              <ServiceSelection />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/booking/barbers" 
          element={
            <ProtectedRoute>
              <BarberSelection />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/booking/form" 
          element={
            <ProtectedRoute>
              <BookingForm />
            </ProtectedRoute>
          } 
        />
        
        {/* Fallback route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default AppRoutes;
