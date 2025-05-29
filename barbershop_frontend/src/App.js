// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import AdminLayout from './pages/admin/AdminLayout';
import Dashboard from './pages/admin/Dashboard';
import BarberManagement from './pages/admin/BarberManagement';
import ServiceManagement from './pages/admin/ServiceManagement';
import AppointmentManagement from './pages/admin/AppointmentManagement';
import Login from './pages/Login/Login';
import PrivateRoute from './components/PrivateRoute';
import Home from './pages/Home/Home';
import Register from './pages/Register/Register';
import BookingSection from './pages/Booking/BookingSection';
import ServiceSelection from './pages/Booking/ServiceSelection';
import BarberSelection from './pages/Booking/BarberSelection';
import BookingForm from './pages/Booking/BookingForm';
import BookingConfirmation from './pages/Booking/BookingConfirmation';
import UserAppointments from './pages/UserAppointments';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Home />} />
          
          {/* Admin Routes */}
          <Route
            path="/admin"
            element={
              <PrivateRoute>
                <AdminLayout>
                  <Dashboard />
                </AdminLayout>
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/barbers"
            element={
              <PrivateRoute>
                <AdminLayout>
                  <BarberManagement />
                </AdminLayout>
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/services"
            element={
              <PrivateRoute>
                <AdminLayout>
                  <ServiceManagement />
                </AdminLayout>
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/appointments"
            element={
              <PrivateRoute>
                <AdminLayout>
                  <AppointmentManagement />
                </AdminLayout>
              </PrivateRoute>
            }
          />

          {/* Booking Routes */}
          <Route path="/booking" element={<BookingSection />} />
          <Route path="/booking/services" element={<ServiceSelection />} />
          <Route path="/booking/barbers" element={<BarberSelection />} />
          <Route path="/booking/form" element={<BookingForm />} />
          <Route path="/booking/confirmation" element={<BookingConfirmation />} />

          {/* User Appointments Route */}
          <Route path="/appointments" element={<PrivateRoute><UserAppointments /></PrivateRoute>} />

          {/* Redirect unknown route ke home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
