import React from 'react';
import { Link } from 'react-scroll';
import Button from '../../../components/Button/Button';

const HeroSection = () => {
  return (
    <section id="home" className="home-section">
      <div className="home-overlay"></div>
      <div className="home-content">
        <h1>Premium Barbershop Experience</h1>
        <p>Where style meets precision. Get the haircut you deserve.</p>
        <div className="home-buttons">
          <Link to="booking" spy={true} smooth={true} offset={-70} duration={500}>
            <Button type="primary">Book Now</Button>
          </Link>
          <Link to="services" spy={true} smooth={true} offset={-70} duration={500}>
            <Button type="secondary">Our Services</Button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;