import React, { useEffect, useState } from 'react';
import { Card, Tag, message, Spin } from 'antd';
import { getAppointments, getServices } from '../../api';
import { useAuth } from '../../contexts/AuthContext';
import './BarberDashboard.css';

const statusColors = {
  pending: 'gold',
  confirmed: 'blue',
  completed: 'green',
  cancelled: 'red'
};

const BarberDashboard = () => {
  const [appointments, setAppointments] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aptRes, servicesRes] = await Promise.all([
          getAppointments(),
          getServices()
        ]);
        
        // Filter appointments for this barber
        const barberAppointments = aptRes.data.data.filter(
          apt => apt.barber_id === user.id
        );
        
        setAppointments(barberAppointments);
        setServices(servicesRes.data.data);
      } catch (err) {
        message.error('Failed to load appointments');
      }
      setLoading(false);
    };
    fetchData();
  }, [user.id]);

  const getServiceName = (id) => {
    const service = services.find(s => s.id === id);
    return service ? service.name : 'N/A';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('id-ID', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="barber-dashboard">
      <h2>My Appointments</h2>
      <div className="appointments-grid">
        {appointments.map(apt => (
          <Card 
            key={apt.id} 
            className="appointment-card"
            title={
              <div className="card-header">
                <span className="customer-name">{apt.user_name}</span>
                <Tag color={statusColors[apt.status]}>{apt.status.toUpperCase()}</Tag>
              </div>
            }
          >
            <div className="appointment-details">
              <div className="detail-item">
                <span className="label">Date:</span>
                <span className="value">{formatDate(apt.appointment_date)}</span>
              </div>
              <div className="detail-item">
                <span className="label">Time:</span>
                <span className="value">{formatTime(apt.appointment_date)}</span>
              </div>
              <div className="detail-item">
                <span className="label">Service:</span>
                <span className="value">{getServiceName(apt.service_id)}</span>
              </div>
              {apt.notes && (
                <div className="detail-item">
                  <span className="label">Notes:</span>
                  <span className="value">{apt.notes}</span>
                </div>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default BarberDashboard;