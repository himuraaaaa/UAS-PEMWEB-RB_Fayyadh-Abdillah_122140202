import React from 'react';
import { Link } from 'react-scroll';
import './ServiceCard.css';

const ServiceCard = ({ service }) => {
  const { title, description, price, icon } = service;
  
  return (
    <div className="service-card">
      <div className="service-icon">
        <i className={`icon-${icon}`}></i>
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="service-price">{price}</div>
      <Link to="booking" className="service-btn" spy={true} smooth={true} offset={-70} duration={500}>
        Book Now
      </Link>
    </div>
  );
};

export default ServiceCard;