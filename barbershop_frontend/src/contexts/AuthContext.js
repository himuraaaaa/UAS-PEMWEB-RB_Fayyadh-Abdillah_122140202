// src/contexts/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [bookingData, setBookingData] = useState({
    service: null,
    barber: null,
    date: '',
    time: '',
    name: '',
    email: '',
    phone: ''
  });

  // Check if user is logged in on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      try {
        setCurrentUser(JSON.parse(user));
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    
    setLoading(false);
  }, []);

  // Login function
  const login = (userData, token) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setCurrentUser(userData);
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setCurrentUser(null);
    // Reset booking data on logout
    setBookingData({
      service: null,
      barber: null,
      date: '',
      time: '',
      name: '',
      email: '',
      phone: ''
    });
  };

  // Update booking data
  const updateBookingData = (data) => {
    setBookingData(prev => ({
      ...prev,
      ...data
    }));
  };

  const value = {
    currentUser,
    login,
    logout,
    isAuthenticated: !!currentUser,
    bookingData,
    updateBookingData
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
