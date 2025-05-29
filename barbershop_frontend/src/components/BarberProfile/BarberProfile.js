import React from 'react';
import './BarberProfile.css';

const BACKEND_URL = "http://localhost:6543";

const BarberProfile = ({ barber }) => {
  const { name, position, image, social } = barber;
  
  return (
     <div className="team-member">
      <div className="member-image">
        <img 
          src={image && !image.startsWith('http') ? `${BACKEND_URL}/assets/barbers/${image}` : image} 
          alt={name} 
          style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
        />
        <div className="member-social">
          <a href={social?.instagram || '#'}><i className="fab fa-instagram"></i></a>
          <a href={social?.facebook || '#'}><i className="fab fa-facebook-f"></i></a>
          <a href={social?.twitter || '#'}><i className="fab fa-twitter"></i></a>
        </div>
      </div>
      <h4>{name}</h4>
      <p>{position}</p>
    </div>
  );
};

export default BarberProfile;