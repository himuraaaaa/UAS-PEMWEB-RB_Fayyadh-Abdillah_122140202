// src/components/ServiceCard/ServiceCard.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './ServiceCard.css';

const ServiceCard = ({ service }) => {
  const { title, name, description, price } = service;
  const { isAuthenticated } = useAuth();
  
  return (
    <div className="service-card">
      <div className="service-content">
        <h2>{service.name || service.title }</h2>
        <p>{description}</p>
        <div className="service-price">${price}</div>
      </div>
      <div className="service-btn-container">
        {isAuthenticated ? (
          <Link to="/booking/services" className="service-btn">Book Now</Link>
        ) : (
          <Link to="/login?redirect=/booking/services" className="service-btn">Login to Book</Link>
        )}
      </div>
    </div>
  );
};

export default ServiceCard;
