// src/pages/Home/sections/HeroSection.js
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Link as ScrollLink } from 'react-scroll';
import Button from '../../../components/Button/Button';
import { useAuth } from '../../../contexts/AuthContext';

const HeroSection = () => {
  const { isAuthenticated } = useAuth();

  return (
    <section id="home" className="home-section">
      <div className="home-overlay"></div>
      <div className="home-content">
        <h1>Premium Barbershop Experience</h1>
        <p>Where style meets precision. Get the haircut you deserve.</p>
        <div className="home-buttons">
          {isAuthenticated ? (
            <RouterLink to="/booking/services">
              <Button type="primary">Book Now</Button>
            </RouterLink>
          ) : (
            <RouterLink to="/login">
              <Button type="primary">Login to Book</Button>
            </RouterLink>
          )}
          <ScrollLink to="services" spy={true} smooth={true} offset={-70} duration={500}>
            <Button type="secondary">Our Services</Button>
          </ScrollLink>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
