import React from 'react';
import HeroSection from './sections/HeroSection';
import ServicesSection from './sections/ServicesSection';
import GallerySection from './sections/GallerySection';
import AboutSection from './sections/AboutSection';
import BookingSection from './sections/BookingSection';
import ContactSection from './sections/ContactSection';
import './Home.css';

const Home = () => {
  return (
    <main className="home-page">
      <HeroSection />
      <ServicesSection />
      <GallerySection />
      <AboutSection />
      <ContactSection />
    </main>
  );
};

export default Home;
