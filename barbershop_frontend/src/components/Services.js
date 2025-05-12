// Services.js
import React from 'react';
import './Services.css';

const Services = () => {
  const services = [
    {
      id: 1,
      title: 'Classic Haircut',
      description: 'Traditional haircut with clippers and scissors for a clean, classic look.',
      price: 'Rp 80.000',
      icon: 'scissors'
    },
    {
      id: 2,
      title: 'Beard Trim',
      description: 'Professional beard shaping and trimming to enhance your facial features.',
      price: 'Rp 50.000',
      icon: 'razor'
    },
    {
      id: 3,
      title: 'Hot Towel Shave',
      description: 'Luxurious straight razor shave with hot towel treatment for ultimate relaxation.',
      price: 'Rp 70.000',
      icon: 'towel'
    },
    {
      id: 4,
      title: 'Hair Coloring',
      description: 'Professional hair coloring service with premium products for vibrant results.',
      price: 'Rp 150.000',
      icon: 'color'
    },
    {
      id: 5,
      title: 'Kids Haircut',
      description: 'Gentle and patient haircut service for children under 12.',
      price: 'Rp 60.000',
      icon: 'kid'
    },
    {
      id: 6,
      title: 'Hair Treatment',
      description: 'Revitalizing hair treatments to restore shine and health to your hair.',
      price: 'Rp 120.000',
      icon: 'treatment'
    }
  ];

  return (
    <section id="services" className="services-section">
      <div className="container">
        <div className="section-header">
          <h2>Our Services</h2>
          <p>Professional haircuts and grooming services for the modern gentleman</p>
        </div>
        <div className="services-grid">
          {services.map(service => (
            <div className="service-card" key={service.id}>
              <div className="service-icon">
                <i className={`icon-${service.icon}`}></i>
              </div>
              <h3>{service.title}</h3>
              <p>{service.description}</p>
              <div className="service-price">{service.price}</div>
              <a href="#booking" className="service-btn">Book Now</a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;
