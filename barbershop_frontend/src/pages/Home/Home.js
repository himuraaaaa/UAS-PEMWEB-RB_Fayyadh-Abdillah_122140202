import React from 'react';
import Navbar from '../../components/Navbar/Navbar';
import Footer from '../../components/Footer/Footer';
import HeroSection from './sections/HeroSection';
import ServicesSection from './sections/ServicesSection';
import GallerySection from './sections/GallerySection';
import AboutSection from './sections/AboutSection';
import ContactSection from './sections/ContactSection';
import './Home.css';

const Home = () => {
  return (
    <>
      <Navbar />
      <main className="home-page">
        <HeroSection />
        <ServicesSection />
        <GallerySection />
        <AboutSection />
        <ContactSection />
      </main>
      <Footer />
    </>
  );
};

export default Home;
