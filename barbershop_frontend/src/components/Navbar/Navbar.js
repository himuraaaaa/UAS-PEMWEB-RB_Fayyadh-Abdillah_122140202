// src/components/Navbar/Navbar.js
import React, { useState, useEffect } from 'react';
import { Link as ScrollLink } from 'react-scroll';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Navbar.css';
import { UserOutlined } from '@ant-design/icons';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const isHomePage = location.pathname === '/';

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

  useEffect(() => {
    if (!profileMenuOpen) return;
    function handleClickOutside(event) {
      const dropdown = document.querySelector('.profile-dropdown');
      const btn = document.querySelector('.profile-btn');
      if (dropdown && !dropdown.contains(event.target) && btn && !btn.contains(event.target)) {
        setProfileMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [profileMenuOpen]);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleLogout = () => {
    logout();
    // Redirect to home page if not already there
    if (location.pathname !== '/') {
      window.location.href = '/';
    }
  };

  const handleProfileClick = () => {
    setProfileMenuOpen(!profileMenuOpen);
  };

  const handleMyAppointments = () => {
    setProfileMenuOpen(false);
    setMenuOpen(false);
    window.location.href = '/appointments';
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="container navbar-container">
        <div className="logo">
          <RouterLink to="/">
            <h1>BarberStyle</h1>
          </RouterLink>
        </div>
        <div className={`menu-icon ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <ul className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          {isHomePage ? (
            // Home page navigation with smooth scroll
            <>
              <li className="nav-item">
                <ScrollLink to="home" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
                  Home
                </ScrollLink>
              </li>
              <li className="nav-item">
                <ScrollLink to="services" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
                  Services
                </ScrollLink>
              </li>
              <li className="nav-item">
                <ScrollLink to="gallery" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
                  Gallery
                </ScrollLink>
              </li>
              <li className="nav-item">
                <ScrollLink to="about" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
                  About Us
                </ScrollLink>
              </li>
              <li className="nav-item">
                <ScrollLink to="contact" spy={true} smooth={true} offset={-70} duration={500} onClick={() => setMenuOpen(false)}>
                  Contact Us
                </ScrollLink>
              </li>
            </>
          ) : (
            // Other pages navigation with router links
            <>
              <li className="nav-item">
                <RouterLink to="/" onClick={() => setMenuOpen(false)}>
                  Home
                </RouterLink>
              </li>
              <li className="nav-item">
                <RouterLink to="/#services" onClick={() => setMenuOpen(false)}>
                  Services
                </RouterLink>
              </li>
              <li className="nav-item">
                <RouterLink to="/#about" onClick={() => setMenuOpen(false)}>
                  About Us
                </RouterLink>
              </li>
              <li className="nav-item">
                <RouterLink to="/#contact" onClick={() => setMenuOpen(false)}>
                  Contact Us
                </RouterLink>
              </li>
            </>
          )}
          
          <li className="nav-item book">
            <RouterLink to="/booking/services" onClick={() => setMenuOpen(false)}>
              Book
            </RouterLink>
          </li>
          
          {isAuthenticated ? (
            <li className="nav-item profile-menu">
              <button className="profile-btn" onClick={handleProfileClick}>
                <UserOutlined style={{ fontSize: 20 }} />
              </button>
              {profileMenuOpen && (
                <div className="profile-dropdown">
                  <button onClick={handleMyAppointments} className="dropdown-item">My Appointments</button>
                  <button onClick={handleLogout} className="dropdown-item">Logout</button>
                </div>
              )}
            </li>
          ) : (
            <li className="nav-item login">
              <RouterLink to="/login" onClick={() => setMenuOpen(false)}>
                Login
              </RouterLink>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
