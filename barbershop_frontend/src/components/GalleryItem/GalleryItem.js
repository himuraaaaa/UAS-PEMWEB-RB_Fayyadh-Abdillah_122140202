import React from 'react';
import './GalleryItem.css';

const GalleryItem = ({ image }) => {
  const { src, alt } = image;
  
  return (
    <div className="gallery-item">
      <img src={src} alt={alt} />
      <div className="gallery-overlay">
        <h3>{alt}</h3>
      </div>
    </div>
  );
};

export default GalleryItem;