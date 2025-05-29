// Lanjutan src/components/ServiceCard/ServiceCard.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './ServiceCard.css';

const ServiceCard = ({ service }) => {
  const { title, description, price, icon } = service;
  const { isAuthenticated } = useAuth();
  
  return (
    <div className="service-card">
      <h2>{service.name || service.title}</h2>
      <p>{description}</p>
      <div className="service-price">${price}</div>
      {isAuthenticated ? (
        <Link to="/booking/services" className="service-btn">Book Now</Link>
      ) : (
        <Link to="/login?redirect=/booking/services" className="service-btn">Login to Book</Link>
      )}
    </div>
  );
};

export default ServiceCard;
