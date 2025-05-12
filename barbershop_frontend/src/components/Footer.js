// Footer.js
import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-logo">
            <h2>BarberStyle</h2>
            <p>Premium barbershop experience for the modern gentleman.</p>
            <div className="social-links">
              <a href="#"><i className="fab fa-facebook-f"></i></a>
              <a href="#"><i className="fab fa-instagram"></i></a>
              <a href="#"><i className="fab fa-twitter"></i></a>
              <a href="#"><i className="fab fa-youtube"></i></a>
            </div>
          </div>
          
          <div className="footer-links">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#services">Services</a></li>
              <li><a href="#gallery">Gallery</a></li>
              <li><a href="#about">About Us</a></li>
              <li><a href="#contact">Contact</a></li>
              <li><a href="#booking">Book Now</a></li>
            </ul>
          </div>
          
          <div className="footer-contact">
            <h3>Contact Us</h3>
            <p><i className="fas fa-map-marker-alt"></i> 123 Barber Street, Jakarta, Indonesia</p>
            <p><i className="fas fa-phone"></i> +62 123 456 7890</p>
            <p><i className="fas fa-envelope"></i> info@barberstyle.com</p>
            <p><i className="fas fa-clock"></i> Mon - Sat: 9:00 AM - 8:00 PM</p>
          </div>
          
          <div className="footer-newsletter">
            <h3>Newsletter</h3>
            <p>Subscribe to our newsletter to get updates on our latest offers!</p>
            <form className="newsletter-form">
              <input type="email" placeholder="Enter your email" required />
              <button type="submit"><i className="fas fa-paper-plane"></i></button>
            </form>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2025 BarberStyle. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
