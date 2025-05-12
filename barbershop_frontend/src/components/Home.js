// Home.js
import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <section id="home" className="home-section">
      <div className="home-overlay"></div>
      <div className="home-content">
        <h1>Premium Barbershop Experience</h1>
        <p>Where style meets precision. Get the haircut you deserve.</p>
        <div className="home-buttons">
          <a href="#booking" className="btn btn-primary">Book Now</a>
          <a href="#services" className="btn btn-secondary">Our Services</a>
        </div>
      </div>
    </section>
  );
};

export default Home;
