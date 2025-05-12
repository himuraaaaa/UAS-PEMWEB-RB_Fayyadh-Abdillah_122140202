// Navbar.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-scroll';
import './Navbar.css';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container">
        <div className="logo">
          <h1>BarberStyle</h1>
        </div>
        <div className={`menu-icon ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <ul className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          <li className="nav-item">
            <Link to="home" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link to="services" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
              Services
            </Link>
          </li>
          <li className="nav-item">
            <Link to="gallery" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
              Gallery
            </Link>
          </li>
          <li className="nav-item">
            <Link to="about" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
              About Us
            </Link>
          </li>
          <li className="nav-item">
            <Link to="contact" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
              Contact Us
            </Link>
          </li>
          <li className="nav-item book">
            <Link to="booking" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
              Book
            </Link>
          </li>
          <li className="nav-item login">
            <a href="/login">Login</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
